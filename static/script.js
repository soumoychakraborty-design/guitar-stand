
let firstClick = true;
function showTiles() {
    firstClick=true;
    document.querySelector('.page-description').style.display='none';
    document.getElementById('tilesContainer').style.display='block';
}
function switchContent(id) {
    const panel = document.getElementById(id);
    panel.style.display = (panel.style.display === 'block') ? 'none' : 'block';
}
function openAbout(){ document.getElementById('aboutPanel').style.width='300px'; }
function closeAbout(){ document.getElementById('aboutPanel').style.width='0'; }
