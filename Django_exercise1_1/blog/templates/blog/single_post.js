function like(slug){
        const data = JSON.stringify({slug: slug})
        $.ajax({
            type: "post",
            url: "{% url 'like' %}",
            data: data,
            success: function (response) {
                console.log(response);
            }});
    }
console.log('hello')
