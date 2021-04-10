window.onload = function() {

    STAR = 'M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.523-3.356c.329-.314.158-.888-.283-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767l-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288l1.847-3.658 1.846 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.564.564 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z';
    STAR_FILL = 'M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.283.95l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z';

    $(document).off('submit');
    $(document).on('submit', '.add-favorite', function(e) {
        let action = $(this).attr('action');
        let target = event.target;
        console.log(action);
        let new_url = "";
        $.ajax({
            url: action,
            method: 'POST',
            data: $(this).serialize(),
            success: function(data) {
                console.log($(this));
                if($(target).find('path').attr('d') != STAR_FILL) {
                    $(target).find('path').attr('d', STAR_FILL);
                }
                $(target).removeClass('add-favorite').addClass('delete-favorite');
                $(target).find('button').removeClass('add-favorite').addClass('delete-favorite');
                action_arr = action.split('/')
                if (data){
                    if (action_arr.includes('jobseeker'))
                        new_url = '/jobseeker/' + action_arr[2] + '/favorite/' + data.id + '/delete/';
                    else if (action_arr.includes('employer'))
                        new_url = '/employer/' + action_arr[2] + '/favorite_' + data.id + '/delete/';
                    $(target).attr('action', new_url);
                }
                console.log('created successfully');
            }
        });
        e.preventDefault();
    });

    $(document).on('submit', '.delete-favorite', function(e) {
        let action = $(this).attr('action');
        console.log(action);
        let target = event.target;
        let new_url = "";
        if (target){
            $.ajax({
                url: action,
                method: 'POST',
                data: $(this).serialize(),
                success: function() {
                    if($(target).find('path').attr('d') != STAR) {
                        $(target).find('path').attr('d', STAR);
                    }
                    $(target).removeClass('delete-favorite').addClass('add-favorite');
                    $(target).find('button').removeClass('delete-favorite').addClass('add-favorite');
                    action_arr = action.split('/')
                    if (action_arr.includes('jobseeker'))
                        new_url = '/jobseeker/' + action_arr[2] + '/favorite/create/';
                    else if (action_arr.includes('employer'))
                        new_url = '/employer/' + action_arr[2] + '/favorite/create/';
                    $(target).attr('action', new_url);
                    console.log('deleted favorite');
                }
            });
        }
        e.preventDefault();
    });

};

$('.bi-sliders').on('click', function() {
    $('.extend').css('display', 'block');
    $('label[for=search-field]').css('display', 'inline');
    $(this).css('opacity', 0);
//    $('#search-field').attr('required', 'required');
    $('.button-search').css('margin-left', '1.3rem');
//    $('#city').attr('required', 'required');
//    $('#sex').attr('required', 'required');
//    $('#salary').attr('required', 'required');
//    $('#from_date').attr('required', 'required');
//    $('#till_date').attr('required', 'required');
})

$('.share').on('click', function() {
    $('.share-icons').toggleClass("active");
    return false;
});

