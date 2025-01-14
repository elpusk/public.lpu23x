async function fetchData() {
    try {
        const response = await fetch('./js/data.json');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// JSON 데이터를 HTML 테이블로 변환하는 함수
function jsonToTable(jsonData) {
    const table = document.getElementById('dataTable');
    const thead = document.getElementById('dataHead');
    const tbody = document.getElementById('dataBody');

    // 테이블 헤더 생성
    const headerRow = document.createElement('tr');
    const headers = ["순번", ...jsonData.head];
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // 테이블 바디 생성
    jsonData.body.forEach((item, index) => {
        const row = document.createElement('tr');
        const serialNumberCell = document.createElement('td');
        serialNumberCell.textContent = index + 1;
        row.appendChild(serialNumberCell);
        
        Object.values(item).forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            row.appendChild(td);
        });
        tbody.appendChild(row);
    });
    
    table.appendChild(thead);
    table.appendChild(tbody);
    return table;
}

// fetchData 함수를 사용하여 데이터를 가져오고 테이블을 생성하여 추가
async function init() {
    const data = await fetchData();
    if (data) {
        const table = jsonToTable(data);
    }
}
