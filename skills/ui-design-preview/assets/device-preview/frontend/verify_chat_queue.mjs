import assert from 'node:assert/strict';
import { submitMessage, finishMessage, runQueuedMessage } from './src/chat_queue.js';

let state = { messages: [], form: { message: 'first' }, chatContext: [] };
state = submitMessage(state, { text: 'first' });
const firstRun = state.chatRun.id;
state = submitMessage(state, { text: 'second' });
state = submitMessage(state, { text: 'third' });
assert.deepEqual(state.chatQueue.map(item => item.text), ['second', 'third']);
state = finishMessage(state, firstRun);
assert.equal(state.messages.at(-1).text, 'second');
assert.deepEqual(state.chatQueue.map(item => item.text), ['third']);

const activeRun = state.chatRun.id;
const immediate = runQueuedMessage(state, state.chatQueue[0].id);
assert.equal(immediate.messages.at(-1).text, 'third');
assert.equal(immediate.chatQueue.length, 0);
assert.equal(finishMessage(immediate, activeRun), immediate);
assert.equal(runQueuedMessage(immediate, 'missing'), immediate);

const paused = finishMessage({ ...state, queuePaused: true }, activeRun);
assert.equal(paused.chatRun, null);
assert.equal(paused.chatQueue[0].text, 'third');
console.log('PASS: FIFO drain, pause, immediate send and stale completion guard');
