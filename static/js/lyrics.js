const alphaBack = 0.2, alphaFocus = 1.0;

let alphas = [];
let toAlphas = [];

let focusRows = [];
let rows = [0];

let lyricsLoaded = false;

function initLyrics(ctx) {
  alphas = [];
  toAlphas = [];

  for (let i = 0; i < texts.length; ++i) {
    alphas.push(alphaBack);
    toAlphas.push(alphaBack);
  }

  lyricsLoaded = true;
}

let baseRow = 0;

function renderLyrics(cvs, ctx, scrW, scrH, texts, pointer, textColor, bgColor) {
  if (!lyricsLoaded)
    return;

  let col = 0;
  let row = 0;

  const ox = scrW / 6;
  const width = scrW / 3 * 2;

  focusRows = [];
  rows = [0];

  for (let i = 0; i < texts.length; ++i) {
    const text = texts[i];
    ctx.font = "normal 30px 'Yu Gothic'";
    ctx.textAlign = "left";
    const metrics = ctx.measureText(text);

    col += metrics.width;

    if (col > width || text === '\n') {
      row += 30;
      rows.push(row);
      col = 0;

      if (text !== '\n')
        --i;

      continue;
    }

    focusRows.push(rows.length - 1);
  }

  col = 0;
  row = 0;

  for (let i = 0; i < texts.length; ++i) {
    const text = texts[i];
    ctx.font = "normal 30px 'Yu Gothic'";
    ctx.textAlign = "left";
    const metrics = ctx.measureText(text);

    if (col + metrics.width > width || text === '\n') {
      row += 30;
      col = 0;

      if (text !== '\n')
        --i;

      continue;
    }

    if (Math.abs(rows.indexOf(row) - focusRows[pointer]) <= 2) {
      ctx.font = "normal 30px 'Yu Gothic'";
      ctx.fillStyle = hex2rgba(textColor, alphas[i]);
      ctx.textAlign = "left";
      ctx.fillText(text, ox + col, row - baseRow + 220);
    }

    col += metrics.width;
  }

  ctx.fillStyle = hex2rgba(bgColor, 1.0);
  ctx.fillRect(ox, 250 + 15, width, 100);
  ctx.fillRect(ox, 0, width, 220 - 15 - 45);

  baseRow = morph(baseRow, rows[focusRows[pointer]], 20);

  if (!pointer) {
    baseRow = morph(baseRow, rows[0], 2);
    //baseRow = rows[0];
  }

  alphaTimeStep(alphas, toAlphas, texts, pointer);
}

function alphaTimeStep(alphas, toAlphas, texts, pointer) {
  for (let i = 0; i < texts.length; ++i) {
    alphas[i] = morph(alphas[i], toAlphas[i], 5);

    toAlphas[i] = i == pointer ? alphaFocus : alphaBack;
  }
}

function morph(from, to, d) {
  return from + (to - from) / d;
}

function hex2rgba(hex, alpha = 1) {

  // ロングバージョンの場合（例：#FF0000）
  let r = hex.match(/^#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i)
  let c = null
  if (r) {
    c = r.slice(1, 4).map(function (x) { return parseInt(x, 16) })
  }
  // ショートバージョンの場合（例：#F00）
  r = hex.match(/^#([0-9a-f])([0-9a-f])([0-9a-f])$/i)
  if (r) {
    c = r.slice(1, 4).map(function (x) { return 0x11 * parseInt(x, 16) })
  }
  // 該当しない場合は、nullを返す.
  if (!c) {
    return null
  }
  return `rgba(${c[0]}, ${c[1]}, ${c[2]}, ${alpha})`
}