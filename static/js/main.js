let texts = [""];

const initialSentence =
	"Flash Readingは、語句を連続でフラッシュ表示する「高速逐次視覚提示」を用いてテキストを高速に読むことを可能にしたアプリです。\
PDFや写真をテキストエリアにドラッグ & ドロップすると文字を読み取ることができます。";

let pointer = 0;

let spanMs = 250;

let jumpMs = 3000;

let isParse = false;

let lastDate = new Date();

let bgColor = "#fefefe";
let textColor = "#282828";
let textSize = 30;
let lastText = null;

function render() {
	const cvs = document.getElementById("canvas");
	const ctx = cvs.getContext("2d");
	const scrW = parseInt(cvs.style.width.slice(0, -2));
	const scrH = parseInt(cvs.style.height.slice(0, -2));

	ctx.clearRect(0, 0, scrW, scrH);

	renderLyrics(cvs, ctx, scrW, scrH, texts, pointer, textColor, bgColor);

	ctx.font = "normal " + textSize + "px 'Yu Gothic'";
	ctx.fillStyle = textColor;
	ctx.textAlign = "center";

	ctx.fillText(texts[pointer], scrW / 2, 100 + (textSize / 2));

	let nowDate = new Date();

	if (nowDate - lastDate >= spanMs && isParse == false) {
		pointer = (pointer + 1) % texts.length;
		lastDate = nowDate;
	}

	requestAnimationFrame(render);
}

window.addEventListener("load", () => {
	sizing();

	//cvs.scale(3, 3);

	function sizing() {
		let cvs = document.getElementById("canvas");
		let ctx = cvs.getContext('2d');
		let cntr = document.getElementById("container");

		const dpr = window.devicePixelRatio || 1;

		const width = cntr.offsetWidth;
		const height = cntr.offsetHeight;

		cvs.width = width * dpr;
		cvs.height = height * dpr;

		ctx.scale(dpr, dpr);

		cvs.style.width = width + 'px';
		cvs.style.height = height + 'px';
	}

	window.addEventListener("resize", function () {
		!window.requestAnimationFrame
			? setTimeout(sizing, 300)
			: window.requestAnimationFrame(sizing);
	});

	render();

	onSliderInput(spanMs);
	onTextSliderInput(textSize);

	if (!canInsert) {
		const invisibleList = ['label-text', 'main-text', 'btn-read-start', 'btn-doc-save'];

		for (let domId of invisibleList)
			document.getElementById(domId).style.display = 'none';

		texts = docObj.units.map(unit => unit.content);
		initAlpha(texts);
		pointer = docObj.doc.current_pos;
	} else {
		const invisibleList = ['btn-pos-save'];

		for (let domId of invisibleList)
			document.getElementById(domId).style.display = 'none';

		onSubmit(initialSentence);
	}

	const spans = document.getElementsByClassName("color-box");

	for (let i = 0; i < spans.length; ++i) {
		const { hex } = spans[i].dataset;

		spans[i].style.backgroundColor = `#${hex}`;
		spans[i].classList.add("fadeIn");
		spans[i].parentNode.parentNode.classList.add("flipIn");
	}
});

function onSliderInput(value) {
	spanMs = value;

	const message = "読み上げる間隔：" + spanMs + " ms";

	document.getElementById("read-speed").innerText = message;
}

let baseUrl;

async function onSubmit(orgText) {
	const apiUrl = baseUrl + "result";

	let text;

	if (!orgText) {
		const textareaDom = document.getElementById("main-text");
		text = textareaDom.value;
		lastText = text;
	} else {
		text = orgText;
	}

	const paramObj = {
		text: text,
	};
	const method = "POST";
	const headers = {
		Accept: "application/json",
		"Content-Type": "application/json",
	};
	const body = JSON.stringify(paramObj);

	console.log("onSubmit");

	const response = await fetch(apiUrl, { method: method, headers: headers, body: body });
	const res = await response.json();

	texts = res.text;
	initAlpha(texts);
	console.log(res.text);
	pointer = 0;
}

function onParse() {
	if (isParse == true) {
		lastDate = new Date();

		isParse = false;
	} else {
		isParse = true;
	}
}

function onReset() {
	lastDate = new Date();
	pointer = 0;
}

function onBack() {
	if (spanMs * pointer < 1000) {
		if (texts.length * spanMs > jumpMs) {
			pointer = texts.length - Math.floor(jumpMs / spanMs);
		} else {
			pointer = 0;
		}
	} else if (spanMs * pointer < jumpMs) {
		pointer = 0;
	} else {
		pointer = pointer - Math.floor(jumpMs / spanMs);
	}
}

function onSkip() {
	lastDate = new Date();
	pointer = (pointer + Math.floor(jumpMs / spanMs)) % texts.length;
}

function setColor(colorBg, colorTxt) {
	bgColor = colorBg;
	textColor = colorTxt;

	document.getElementById("body").style.backgroundColor = bgColor;

	var elements = document.getElementsByClassName("btn-col");

	if (bgColor == "#316745" || bgColor == "#1a110d") {
		document.getElementById("body").style.color = "#ffffff";
		document.getElementById("col-title").style.borderBottom =
			"1px solid #eeeeee";

		for (let element of elements) {
			element.classList.remove("btn-outline-dark");
			element.classList.add("btn-outline-light");
		}
	} else {
		document.getElementById("body").style.color = "#000000";
		document.getElementById("col-title").style.borderBottom =
			"1px solid #7f7975";

		for (let element of elements) {
			element.classList.remove("btn-outline-light");
			element.classList.add("btn-outline-dark");
		}
	}
}

function onTextSliderInput(size) {
	textSize = size;

	const message = "テキストサイズ：" + size + " px";

	document.getElementById("text-size").innerText = message;
}

// param required: content, name, current_pos, split_units
async function onSave() {
	const apiUrl = baseUrl + "insert";

	let prevText = lastText;

	// Validation
	if (!lastText) {
		const textareaDom = document.getElementById("main-text");
		const text = textareaDom.value;

		if (!text)
			return alert('テキストが入力されていません');

		console.log(text);

		lastText = text;

		await onSubmit(text);

		console.log("ended");
	}
	if (texts.length == 1 && texts[0] === "")
		return alert('エラーが発生しました');
	if (pointer < 0 || pointer >= texts.length)
		return alert('エラーが発生しました');
	if (texts.length > 1000)
		return alert('文書が長すぎます');

	if (!(name = window.prompt('保存する文書の名前を入力してください'))) {
		lastText = prevText;

		return alert('名前が空です');
	}

	if (name && name.length) {
		const paramObj = {
			content: lastText,
			split_units: texts,
			current_pos: pointer,
			name: name,
		};
		const method = "POST";
		const headers = {
			Accept: "application/json",
			"Content-Type": "application/json",
		};
		const body = JSON.stringify(paramObj);

		console.log(name);

		console.log("onSave");

		await fetch(apiUrl, { method: method, headers: headers, body: body }).then(_ => {
			window.location.href = baseUrl + 'list';
		});
	} else {
		lastText = prevText;

		return alert('名前が空です');
	}
}

// param required: uuid
function onDelete(uuid) {
	const apiUrl = baseUrl + "delete";

	// Validation
	if (!uuid)
		return alert("エラーが発生しました");

	const paramObj = {
		uuid: uuid,
	};
	const method = "POST";
	const headers = {
		Accept: "application/json",
		"Content-Type": "application/json",
	};
	const body = JSON.stringify(paramObj);

	console.log("onDelete");

	fetch(apiUrl, { method: method, headers: headers, body: body }).then(_ => {
		location.reload();
	});
}

// param required: uuid, current_pos
function onPosSave() {
	const apiUrl = baseUrl + "update";

	// Validation
	if (!docObj.doc.uuid)
		return alert("エラーが発生しました");
	if (pointer < 0 || pointer >= texts.length)
		return alert("エラーが発生しました");

	const paramObj = {
		uuid: docObj.doc.uuid,
		current_pos: pointer,
	};
	const method = "POST";
	const headers = {
		Accept: "application/json",
		"Content-Type": "application/json",
	};
	const body = JSON.stringify(paramObj);

	console.log("onPosSave");

	fetch(apiUrl, { method: method, headers: headers, body: body }).then(_ => {
		window.location.href = baseUrl + 'list';
	});
}

function summarize(str) {
	return str.substr(0, 140) + "...";
}

function formatDate(dateStr) {
	const index = dateStr.lastIndexOf('+');

	let ret = dateStr.substr(0, index);

	ret = ret.replace('T', ' ');

	return ret;
}