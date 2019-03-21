    // Initialize
    $(document).ready(function(){
        $('.venobox').venobox({
            'closeBackground': 'transparent',
            'spinner': 'wandering-cubes',
        });
    });
    
    // Change Search Type
    var dropdownMenus = document.getElementsByClassName('search-type');
    var params = document.getElementById('type-result');
    var dropdownBtn = document.getElementById('dropdown-search');

    for (var i = 0; i < dropdownMenus.length; i++) {
        dropdownMenus[i].addEventListener('click', onMenuSelected);
    }

    function onMenuSelected(e) {
        var sender = e.target;
        dropdownBtn.children[0].innerHTML = e.target.innerText + ' <i class="icon icon-caret"></i>';
        params.value = sender.dataset['searchType'];
    }

    // Customize Enter Event
    var inputSearch = document.getElementById('form-search');
    inputSearch.addEventListener('submit', onSearch);

    function onSearch(e) {
        var validSubmit = false;
        var inputSearch = document.getElementById('input-search');
        if (params.value === '-1') {
            Swal.fire({
                title: 'Failed!',
                text: '검색 설정이 선택되지 않았어요!',
                type: 'error',
                confirmButtonText: '확인'
            })
        }
        else if (inputSearch.value.trim() === '') {
            Swal.fire({
                title: 'Failed!',
                text: '검색어를 비워둘 수는 없어요!',
                type: 'error',
                confirmButtonText: '확인'
            })
        }
        else validSubmit = true;
    
        if (!validSubmit) e.preventDefault();
    }

    // Detect Auto-Complete
    document.addEventListener("DOMContentLoaded", function(){
        var result = params.value === '0' ? "채널명" : params.value === '1' ? "게임명" : "검색 설정";
        dropdownBtn.children[0].innerHTML = result + ' <i class="icon icon-caret"></i>';
    });