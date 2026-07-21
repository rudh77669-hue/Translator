const API = "http://127.0.0.1:5000";

const translateBtn = document.getElementById("translateBtn");
const micBtn = document.getElementById("micBtn");
const speakerBtn = document.getElementById("speakerBtn");

translateBtn.addEventListener("click", async () => {

    const text = document.getElementById("user_input").value;

    const src_lang = document.getElementById("src_lang").value;

    const target_lang = document.getElementById("target_lang").value;

    const response = await fetch(API + "/translate", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            text,
            src_lang,
            target_lang

        })

    });

    const data = await response.json();

    if (data.success) {

        document.getElementById("resultBox").style.display = "block";

        document.getElementById("translatedText").innerHTML =
            data.translation;

    }

});

micBtn.addEventListener("click", async () => {

    const response = await fetch(API + "/listen");

    const data = await response.json();

    document.getElementById("user_input").value = data.text;

});
speakerBtn.addEventListener("click", async () => {

    const text =
        document.getElementById("translatedText").innerText;

    const lang =
        document.getElementById("target_lang").value;

    await fetch(API + "/speak", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            text,
            lang

        })

    });

});