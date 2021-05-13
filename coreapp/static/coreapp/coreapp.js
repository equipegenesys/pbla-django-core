// console.log(g_drive_integ_link);
for (let i = 1; i <= 2; i++) {
    const row = document.getElementById(`row-${i}`);
    if (i === 1 && status !== "Integrado") {
        row.addEventListener("click", () => {
            window.location.replace(g_drive_integ_link);
        });
    }
}