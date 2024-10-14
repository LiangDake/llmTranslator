$(document).ready(function() {
    // 处理表单提交
    $('#translateForm').on('submit', function(e) {
        e.preventDefault(); // 阻止默认表单提交
        showTranslationModal(); // 显示翻译中弹窗

        // 使用 AJAX 提交表单
        $.ajax({
            url: $(this).attr('action'), // 获取表单的 action 属性
            method: $(this).attr('method'), // 获取表单的 method 属性
            data: $(this).serialize(), // 序列化表单数据
            success: function(response) {
                // 翻译完成后显示完成弹窗
                showTranslationCompleteModal();
            },
            error: function() {
                alert('翻译失败，请重试。');
                $('#translationModal').modal('hide');
            }
        });
    });

    function showTranslationModal() {
        $('#translationModal').modal('show');
    }

    function showTranslationCompleteModal() {
        $('#translationModal').modal('hide');
        $('#translationCompleteModal').modal('show');
    }
});
