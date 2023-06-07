function call_sw_alert_func(route, id, message) {
     swal({
        title: "Вы уверены?",
        text: message,
        icon: "warning",
        buttons: {
            cancel: "Отмена",
            confirm: "Да"
        },
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    type: 'GET',
                    url: route,
                    success: function (data) {
                        if (route.includes('delete')) {
                            swal({
                                title: "Удаление выполнено!",
                                text: "Ваша вакансия была удалена!",
                                icon: "success",
                                button: "Готово",
                            }).then(() => {
                                window.location.href = '/';
                            });
                            $("#row_" + id).remove();
                        } else if (route.includes('close')) {
                            swal({
                                title: "Готово!",
                                text: "Ваша вакансия была закрыта!",
                                icon: "success",
                                button: "Готово",
                            });
                            $("#change_job_status_" + id).html('<a class="text-white btn btn-success btn-sm" role="button">Снято с публикации</a>')
                        }
                    },
                     error: function () {
                        swal({
                            title: 'Что-то пошло не так!',
                            // text: data.message,
                            timer: '1500'
                        })
                    }
                });
            } else {
                swal("Ваша публикация в безопасности!");
            }
        });
}