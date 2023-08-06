/*
let customMenu = document.createElement('div')
customMenu.style.position = 'absolute'
customMenu.style.zIndex = '10000'
customMenu.style.background = 'rgba(25, 25, 25, 0.7)'
customMenu.style.color = 'lightgrey'
customMenu.style.display = 'none'
customMenu.style.borderRadius = '5px'
customMenu.style.padding = '5px 10px'
document.body.appendChild(customMenu)

function menuItem(text) {
    let elem = document.createElement('div')
    elem.innerText = text
    customMenu.appendChild(elem)
}
menuItem('Delete drawings')
menuItem('Hide all indicators')
menuItem('Save Chart State')

let closeMenu = (event) => {if (!customMenu.contains(event.target)) customMenu.style.display = 'none';}
document.addEventListener('contextmenu', function (event) {
    event.preventDefault(); // Prevent default right-click menu
    customMenu.style.left = event.clientX + 'px';
    customMenu.style.top = event.clientY + 'px';
    customMenu.style.display = 'block';
    document.removeEventListener('click', closeMenu)
    document.addEventListener('click', closeMenu)
    });

*/


class Table {
    constructor(width, height, headings, widths, alignments, position, draggable= false) {
        let tableContainer = document.createElement('div')

        if (draggable) {
            tableContainer.style.position = 'absolute'
            tableContainer.style.cursor = 'move'
        }
        else {
            tableContainer.style.position = 'relative'
            tableContainer.style.float = position
        }

        tableContainer.style.zIndex = '2000'
        tableContainer.style.width = width*100+'%'
        tableContainer.style.height = height*100+'%'

        tableContainer.style.backgroundColor = '#000'
        tableContainer.style.borderRadius = '5px'
        tableContainer.style.color = 'white'
        tableContainer.style.fontSize = '12px'
        tableContainer.style.fontVariantNumeric = 'tabular-nums'

        this.table = document.createElement('table')
        this.table.style.width = '100%'
        this.table.style.borderCollapse = 'collapse'
        this.rows = {}

        this.headings = headings
        this.widths = widths.map((width) => `${width*100}%`)
        this.alignments = alignments

        let head = this.table.createTHead()
        let row = head.insertRow()

        for (let i=0; i<this.headings.length; i++) {
            let th = document.createElement('th')
            th.textContent = this.headings[i]
            th.style.width = this.widths[i]
            th.style.textAlign = 'center'
            row.appendChild(th)
            th.style.border = '1px solid darkgray';
        }

        tableContainer.appendChild(this.table)
        document.getElementById('wrapper').appendChild(tableContainer)

        if (!draggable) return

        let offsetX, offsetY;

        function onMouseDown(event) {
            offsetX = event.clientX - tableContainer.offsetLeft;
            offsetY = event.clientY - tableContainer.offsetTop;

            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        }

        function onMouseMove(event) {
            tableContainer.style.left = (event.clientX - offsetX) + 'px';
            tableContainer.style.top = (event.clientY - offsetY) + 'px';
        }

        function onMouseUp() {
            // Remove the event listeners for dragging
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        }

        tableContainer.addEventListener('mousedown', onMouseDown);


    }
    newRow (vals, id) {
        console.log('yep')
        this.rows[id] = this.table.insertRow()

        for (let i=0; i<vals.length; i++) {
            this.rows[id][this.headings[i]] = this.rows[id].insertCell()
            this.rows[id][this.headings[i]].textContent = vals[i]
            this.rows[id][this.headings[i]].style.width = this.widths[i];
            this.rows[id][this.headings[i]].style.textAlign = this.alignments[i];
            this.rows[id][this.headings[i]].style.border = '1px solid darkgray';
        }
    }
    updateCell(rowId, column, val) {
        this.rows[rowId][column].textContent = val
    }
}
window.Table = Table

// let test = new Table('Symbol', 'Qty', 'P&L')
// test.newRow(123, 'TSLA', '3', '£300')
// test.newRow(123, 'TSLA', '3', '£300')
// test.newRow(123, 'TSLA', '3', '£300')
// test.newRow(123, 'TSLA', '3', '£300')
// test.newRow(123, 'TSLA', '3', '£300')
// test.newRow(123, 'TSLA', '3', '£300')
// test.newRow(123, 'TSLA', '3', '£300')
