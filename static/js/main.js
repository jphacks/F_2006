let texts = [""];

const initialSentence =
	"速読君は、語句を連続でフラッシュ表示する「高速逐次視覚提示」を用いてテキストを高速に読むことを可能にしたアプリです。\
PDFや写真をテキストエリアにドラッグ & ドロップすると文字を読み取ることができます。";

let pointer = 0;

let spanMs = 250;

let isParse = false;

let lastDate = new Date();

function render() {
	const cvs = document.getElementById("canvas");
	const ctx = cvs.getContext("2d");
	const scrW = cvs.width,
		scrH = cvs.height;

	ctx.clearRect(0, 0, scrW, scrH);
	ctx.font = "normal 30px 'Yu Gothic'";
	ctx.fillStyle = "rgb(40, 40, 40)";
	ctx.textAlign = "center";

	ctx.fillText(texts[pointer], scrW / 2, scrH / 2);

	let nowDate = new Date();

	if (nowDate - lastDate >= spanMs && isParse == false) {
		pointer = (pointer + 1) % texts.length;
		lastDate = nowDate;
	}

	requestAnimationFrame(render);
}

window.addEventListener("load", () => {
	sizing();

	function sizing() {
		let cvs = document.getElementById("canvas");
		let cntr = document.getElementById("container");

		cvs.height = cntr.offsetHeight;
		cvs.width = cntr.offsetWidth;
	}

	window.addEventListener("resize", function () {
		!window.requestAnimationFrame
			? setTimeout(sizing, 300)
			: window.requestAnimationFrame(sizing);
	});

	render();

	onSliderInput(spanMs);

	onSubmit(initialSentence);
});

function onSliderInput(value) {
	spanMs = value;

	const message = "読み上げる間隔：" + spanMs + " ms";

	document.getElementById("read-speed").innerText = message;
}

let baseUrl;

function onSubmit(orgText) {
	const apiUrl = baseUrl + "result";

	let text;

	if (!orgText) {
		const textareaDom = document.getElementById("main-text");
		text = textareaDom.value;
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

	fetch(apiUrl, { method: method, headers: headers, body: body }).then(
		(res) => {
			res.json().then((res) => {
				texts = res.text;
				console.log(res.text);
				pointer = 0;
			});
		}
	);
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
