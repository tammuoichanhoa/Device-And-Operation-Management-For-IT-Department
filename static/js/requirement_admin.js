document.addEventListener('DOMContentLoaded', function () {
    const requestTypeSelect = document.querySelector('#id_request_type');
    
    function toggleFields() {
        const type = requestTypeSelect.options[requestTypeSelect.selectedIndex].text.toLowerCase();

        const thanhLyFields = ['id_disposal_date', 'id_disposal_reason'];
        const banGiaoFields = ['id_borrower', 'id_giver', 'id_receiver', 'id_borrow_date', 'id_return_date', 'id_returner'];

        function show(fields) {
            fields.forEach(id => {
                const row = document.querySelector(`#${id}`).closest('.form-row, .form-group');
                if (row) row.style.display = '';
            });
        }

        function hide(fields) {
            fields.forEach(id => {
                const row = document.querySelector(`#${id}`).closest('.form-row, .form-group');
                if (row) row.style.display = 'none';
            });
        }

        hide(thanhLyFields);
        hide(banGiaoFields);

        if (type.includes('TLTB')) {
            show(thanhLyFields);
        } else if (type.includes('BGTB') || type.includes('DDTB')) {
            show(banGiaoFields);
        }
    }

    if (requestTypeSelect) {
        toggleFields();
        requestTypeSelect.addEventListener('change', toggleFields);
    }
});
