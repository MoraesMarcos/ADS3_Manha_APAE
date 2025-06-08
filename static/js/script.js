document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", function () {
            const submitBtn = form.querySelector("[type=submit]");
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.value = "Enviando...";
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const checkAlergia = document.querySelector("#alergia");
    const campoQualAlergia = document.querySelector("#campo-qual-alergia");

    if (checkAlergia && campoQualAlergia) {
        function toggleCampo() {
            campoQualAlergia.style.display = checkAlergia.checked ? "block" : "none";
        }

        checkAlergia.addEventListener("change", toggleCampo);
        toggleCampo(); // Executa ao carregar a página
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const msg = document.querySelector(".mensagem-sucesso");
    if (msg) {
        setTimeout(() => {
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 1000);
        }, 4000); // some depois de 4 segundos
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function (event) {
            const email = form.querySelector("input[name='email']");
            if (email && !email.value.includes("@")) {
                event.preventDefault();
                alert("Por favor, insira um e-mail válido.");
            }
        });
    }
});
