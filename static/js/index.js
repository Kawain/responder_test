//html要素
const allCheck = document.getElementById("allCheck");
const startDiv = document.getElementById("startDiv");
const filterBtn = document.getElementById("filterBtn");
const questionsDiv = document.getElementById("questionsDiv");
const resultDiv = document.getElementById("resultDiv");
const queCode = document.getElementById("queCode");
const ansInput = document.getElementById("ansInput");
const mesP = document.getElementById("mesP");
const giveUpBtn = document.getElementById("giveUpBtn");
const nextBtn = document.getElementById("nextBtn");
//インデックス
let index = 0;
//正解数
let correct = 0;
//全選択と全選択解除
function allChecked(e) {
    const f = e.target.checked;
    const checkboxList = document.getElementsByName("cateCheck");
    for (const v of checkboxList) {
        v.checked = f;
    }
}
//全選択と全選択解除
allCheck.addEventListener("click", allChecked);
//配列をシャッフル
function arrShuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
        let r = Math.floor(Math.random() * (i + 1));
        let tmp = arr[i];
        arr[i] = arr[r];
        arr[r] = tmp;
    }
}
//ギブアップボタン
giveUpBtn.addEventListener("click", () => {
    index++;
    ansInput.value = ansInput.dataset.ans;
    ansInput.disabled = true;
    mesP.innerText = "残念でした";
    giveUpBtn.style.display = "none";
    nextBtn.style.display = "inline";
});
//答える
ansInput.addEventListener("input", (e) => {
    if (e.target.value === ansInput.dataset.ans) {
        ansInput.disabled = true;
        index++;
        correct++;
        mesP.innerText = "正解";
        giveUpBtn.style.display = "none";
        nextBtn.style.display = "inline";
    }
});
//画面表示
function fnDisplay(questions) {
    //問題数
    const number = questions.length;
    //計算
    let average;
    if (index > 0) {
        average = ((correct / index) * 100).toFixed(2);
    } else {
        average = "";
    }
    //終了
    if ((number - 1) < index) {
        giveUpBtn.style.display = "none";
        resultDiv.innerText = `${index}問中${correct}問正解／正解率${average}％でした！`;
        ansInput.style.display = "none";
        document.getElementById("codePre").style.display = "none";
    } else {
        ansInput.focus();
        resultDiv.innerText = `${index}問中${correct}問正解／正解率${average}％　全部で${number}問あります`;
        queCode.innerText = `${questions[index][4]} の問題\n\n${questions[index][2]}`;
        ansInput.dataset.ans = questions[index][1];
    }
}
//問題開催
function fnHeld(questions) {
    //隠す
    startDiv.style.display = "none";
    //表示する
    questionsDiv.style.display = "block";
    //次の問題
    nextBtn.addEventListener("click", () => {
        ansInput.disabled = false;
        mesP.innerText = "";
        queCode.innerText = "";
        ansInput.value = "";
        giveUpBtn.style.display = "inline";
        nextBtn.style.display = "none";
        fnDisplay(questions);
    });
    //1問目
    fnDisplay(questions);
}
//問題をフェッチしてからシャッフルして抽出
async function fnFetch() {
    //フェッチ
    const res = await fetch(`/api/get`);
    //オブジェクト作成
    const data = await res.json();
    //データベースが空
    if (data.length == 0) {
        alert("申し訳ありません。問題がありませんでした。");
        return;
    }
    //シャッフル
    arrShuffle(data);
    //ボタンを有効にする
    filterBtn.disabled = false;
    //開始ボタン
    filterBtn.addEventListener("click", () => {
        //問題を入れる配列
        let questions = [];
        //カテゴリチェックボックス
        let cate = document.getElementsByName("cateCheck");
        for (let v1 of data) {
            for (let v2 of cate) {
                if (v2.checked) {
                    if (v1[3] === parseInt(v2.value)) {
                        questions.push(v1);
                    }
                }
            }
        }
        if (questions.length > 0) {
            fnHeld(questions);
        } else {
            alert("問題がありませんでした");
        }
    });
}

fnFetch();