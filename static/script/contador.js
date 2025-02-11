function iniciarContador() {
    const dataFinal = new Date();
    dataFinal.setDate(dataFinal.getDate() + 6); // 6 dias a partir de hoje
    dataFinal.setHours(dataFinal.getHours() + 18);
    dataFinal.setMinutes(dataFinal.getMinutes() + 48);

    function atualizarContador() {
        const agora = new Date();
        const diferenca = dataFinal - agora;

        if (diferenca <= 0) {
            document.getElementById("dias").textContent = "00";
            document.getElementById("horas").textContent = "00";
            document.getElementById("minutos").textContent = "00";
            return;
        }

        const dias = Math.floor(diferenca / (1000 * 60 * 60 * 24));
        const horas = Math.floor((diferenca % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutos = Math.floor((diferenca % (1000 * 60 * 60)) / (1000 * 60));

        document.getElementById("dias").textContent = String(dias).padStart(2, '0');
        document.getElementById("horas").textContent = String(horas).padStart(2, '0');
        document.getElementById("minutos").textContent = String(minutos).padStart(2, '0');
    }

    atualizarContador();
    setInterval(atualizarContador, 1000);
}

iniciarContador();
