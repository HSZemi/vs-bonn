function toggleTOC(){
    if(document.getElementById("toc").style.display == "none"){
        document.getElementById("toc").style.display = "inline";
        document.getElementById("toctoggle").className = "eye-open";
    } else {
        document.getElementById("toc").style.display = "none";
        document.getElementById("toctoggle").className = "eye-close";
    }
}

const trToString = (tr)=>{
    tds = tr.getElementsByTagName('td');
    console.log(tds);
    return Array.from(tds).map(td => td.textContent).join('|').toLowerCase()
}

const addFilterToLongTables = ()=>{
    const tables = document.getElementsByTagName('table');
    for (const table of tables) {
        const trs = table.getElementsByTagName('tr');
        if (trs.length < 20) {
            continue;
        }
        const input = document.createElement('input');
        input.classList.add('filter-input');
        input.placeholder = 'Filter…';
        input.onkeyup = (e)=>{
            if (e.key === "Escape") {
                e.target.value = '';
            }
            const filter = e.target.value.replace(/ /g, '_').toLowerCase();
            const tr = table.getElementsByTagName('tr');
            
            for (let i = 0; i < tr.length; i++) {
                if (tr[i] !== undefined && !tr[i].classList.contains('header')) {
                    if (trToString(tr[i]).indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }
            }
        }
        table.parentNode.insertBefore(input, table);
    }
}
addFilterToLongTables();
