document.addEventListener('DOMContentLoaded', function () {
    var alertButton = document.getElementById('alertButton');
    if (alertButton) {
        alertButton.addEventListener('click', function() {
            alert('图片已经生成。');
        });
    }
});