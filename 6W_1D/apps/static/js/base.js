$(document).ready(function () {
    $('.llFlaskrArticleForm #content').summernote({
        lang: 'ko-KR',               // default: 'en-US'
        height: 300,                 // set editor height

        minHeight: null,             // set minimum height of editor
        maxHeight: null,             // set maximum height of editor

        focus: true                 // set focus to editable area after initializing summernote
    });

    $('.llFlaskrArticleForm').submit(function () {
        setTimeout(function () {
            $('#content').val($('.llFlaskrArticleForm #content').code());
        }, 50);
    });


});