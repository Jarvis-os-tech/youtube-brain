// ==UserScript==
// @name         yt-brain watch buffer
// @namespace    local.yt-brain
// @version      1.0.0
// @description  POST completed YouTube watches to the local yt-brain webhook.
// @match        *://www.youtube.com/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

// Entry Point B. Complements the Chrome history parser: the webhook fires on
// genuine completion (>=90%), so the buffer is a higher-precision feed than
// history rows, which include stray clicks.
//
// If the webhook is not running, the payload is stored in localStorage and
// flushed on the next visit instead of being lost.

const ENDPOINT = 'http://127.0.0.1:8767/webhook/watch';
const BUFFER_KEY = 'yt-brain:buffer';
const THRESHOLD = 0.9;
const FLUSH_INTERVAL_MS = 15000;

function parseVideoId() {
  const url = new URL(location.href);
  if (url.pathname === '/watch') {
    return url.searchParams.get('v');
  }
  return null;
}

function cleanTitle(t) {
  return (t || 'untitled').replace(/^\(\d+\)\s*/, '').replace(/\s*-\s*YouTube(\s*\(.*?\))?\s*$/, '').trim();
}

function currentTitle() {
  const h1 = document.querySelector('h1.ytd-watch-metadata, h1.title, #title h1');
  return cleanTitle(h1 ? h1.textContent : document.title);
}

function bufferLocally(payload) {
  try {
    const existing = JSON.parse(localStorage.getItem(BUFFER_KEY) || '[]');
    existing.push(payload);
    localStorage.setItem(BUFFER_KEY, JSON.stringify(existing.slice(-500)));
  } catch (e) {
    console.warn('[yt-brain] buffer failed', e);
  }
}

async function post(payload) {
  try {
    const res = await fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      // Opaque response: the server is plain HTTP on loopback.
      mode: 'cors',
    });
    if (!res.ok && res.type !== 'opaque') {
      throw new Error('HTTP ' + res.status);
    }
    return true;
  } catch (e) {
    return false;
  }
}

async function flush() {
  const pending = JSON.parse(localStorage.getItem(BUFFER_KEY) || '[]');
  if (!pending.length) return;
  for (const payload of pending) {
    if (!(await post(payload))) return;  // server still down; retry later
  }
  localStorage.removeItem(BUFFER_KEY);
}

function buildPayload() {
  const videoId = parseVideoId();
  if (!videoId) return null;
  const player = document.querySelector('#movie_player');
  const duration = player && player.getDuration ? player.getDuration() : null;
  return {
    video_id: videoId,
    url: location.href.split('&list=')[0],
    title: currentTitle(),
    duration: duration ? Math.round(duration) : null,
    timestamp: Date.now() / 1000,
  };
}

let sent = new Set();
let lastVideoId = parseVideoId();

function tick() {
  if (location.href.includes('/watch') !== document.URL.includes('/watch')) return;
  const player = document.querySelector('#movie_player');
  if (!player || typeof player.getDuration !== 'function' || typeof player.getCurrentTime !== 'function') return;

  const videoId = parseVideoId();
  if (videoId && videoId !== lastVideoId) {
    lastVideoId = videoId;
    sent = new Set();
  }
  if (!videoId || sent.has(videoId)) return;

  const duration = player.getDuration();
  const current = player.getCurrentTime();
  if (!duration || current / duration < THRESHOLD) return;

  const payload = buildPayload();
  if (!payload) return;
  sent.add(videoId);

  (async () => {
    if (await post(payload)) {
      console.debug('[yt-brain] sent', payload.video_id, payload.title);
    } else {
      bufferLocally(payload);
      console.debug('[yt-brain] webhook down, buffered', payload.video_id);
    }
  })();
}

new MutationObserver(tick).observe(document.documentElement, { childList: true, subtree: true });
setInterval(tick, 1000);
setInterval(flush, FLUSH_INTERVAL_MS);
flush();
