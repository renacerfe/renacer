/*
 * JUEGO VALENTIA BASE - ESCALABLE
 * Autor: Gemini Code Assist
 * Descripción: Motor tipo Valentia (Drag & Drop) en Vanilla JS
 */

const boardCanvas = document.getElementById('board');
const boardCtx = boardCanvas.getContext('2d');

// Referencias a los canvas de las piezas (preview)
const pieceCanvases = [
    document.getElementById('piece-0'),
    document.getElementById('piece-1'),
    document.getElementById('piece-2')
];
const pieceContexts = pieceCanvases.map(c => c.getContext('2d'));

// Definimos el tamaño del bloque base (Resolución interna aumentada)
const BLOCK_SIZE = 40; 
boardCtx.scale(BLOCK_SIZE, BLOCK_SIZE);
pieceContexts.forEach(ctx => ctx.scale(BLOCK_SIZE, BLOCK_SIZE));

// --- CONFIGURACIÓN Y VARIABLES GLOBALES ---

// Configuración del tablero
const BOARD_W = 8;
const BOARD_H = 8;
const BOARD_OFFSET = { x: 0, y: 0 }; // El canvas ahora es SOLO el tablero

// Definición de las piezas (Tetrominós)
// Cada número corresponde a un color en la paleta
const PIECES = {
    '1': [[1]], // Monomino
    '2': [[2, 2]], // Domino
    '3': [[3, 3, 3]], // Trimino
    'T': [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    'O': [[2, 2], [2, 2]],
    'L': [[0, 3, 0], [0, 3, 0], [0, 3, 3]],
    'J': [[0, 4, 0], [0, 4, 0], [4, 4, 0]],
    'I': [[5], [5], [5], [5]], // I vertical simplificada
    'S': [[0, 6, 6], [6, 6, 0], [0, 0, 0]],
    'Z': [[7, 7, 0], [0, 7, 7], [0, 0, 0]],
    '9': [[4,4,4],[4,4,4],[4,4,4]] // Bloque grande 3x3
};

// Colores asociados a los índices de las matrices (null, morado, amarillo, naranja, azul, cyan, verde, rojo)
const COLORS = [
    null,
    '#FF6B6B', // T (Rojo suave)
    '#4ECDC4', // O (Turquesa)
    '#FFE66D', // L (Amarillo pastel)
    '#FF9F43', // J (Naranja)
    '#54A0FF', // I (Azul cielo)
    '#5F27CD', // S (Morado)
    '#C4E538', // Z (Verde lima)
    '#FF9FF3', // 9 (Rosa)
];

// Iconos Bíblicos Vectoriales (SVG Paths 24x24)
const ICONS = {
    1: "M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z", // Corazón (Amor)
    2: "M21.5 11.5c-1.2-.6-2.5-1.1-3.9-1.4 1.4-.3 2.7-.8 3.9-1.4.6-.3 1.5-.8 1.5-1.7 0-1.4-2.5-2.5-5.5-3.3-3.1-.8-6.4-.8-9.5 0C5 4.5 2.5 5.6 2.5 7s2.5 2.5 5.5 3.3c3.1.8 6.4.8 9.5 0l4 4c.4.4 1 .4 1.4 0 .4-.4.4-1 0-1.4l-1.4-1.4z", // Pez (Fe)
    3: "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z", // Estrella (Guía)
    4: "M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z", // Corona (Reino)
    5: "M18.5 12c0-1.7-1.3-3-3-3-.3 0-.6.1-.8.2-.6-1.5-2.1-2.7-3.7-2.7-2.1 0-3.9 1.6-4 3.7 0 .1 0 .2 0 .3-1.9.2-3.4 1.8-3.4 3.8 0 2.1 1.7 3.8 3.8 3.8h10.3c2.1 0 3.8-1.7 3.8-3.8 0-1.3-.6-2.4-1.6-3.1.4-.4.6-.8.6-1.2z", // Nube/Cielo (Paz)
    6: "M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 4h2v5l-1-.5L9 9V4zm9 16H6V4h1v9l3-1.5 3 1.5V4h5v16z", // Libro (Palabra)
    7: "M17 8C8 10 5.9 16.17 3.82 21.34 5.71 20.73 6.63 19.91 17 8z", // Hoja (Creación)
    8: "M11 2h2v6h6v2h-6v12h-2V10H5V8h6z" // Cruz (Salvación)
};

// Estado del juego
const player = {
    score: 0,
    chapterIndex: 0, // Índice del capítulo actual
    inventory: [], // Las 3 piezas disponibles
};

// Datos del Jugador (Personalización)
let playerData = {
    name: "Amigo",
    characterId: 'sheep'
};

// Base de datos de Personajes Acompañantes
const CHARACTERS = [
    { id: 'sheep', name: 'Ovi', icon: '🐑', msgs: ['¡Qué suave!', '¡Tú puedes!', '¡Beeee-llísimo!', '¡Sigue así!'] },
    { id: 'dove', name: 'Paz', icon: '🕊️', msgs: ['Vuela alto', '¡Paz y amor!', '¡Increíble!', '¡Muy bien!'] },
    { id: 'star', name: 'Estrellita', icon: '⭐', msgs: ['¡Brillante!', '¡Iluminas todo!', '¡Genial!', '¡Destellante!'] },
    { id: 'explorer', name: 'Noé', icon: '🤠', msgs: ['¡Gran hallazgo!', '¡Sigamos!', '¡Aventura!', '¡Buen camino!'] },
    { id: 'scroll', name: 'Sabio', icon: '📜', msgs: ['Está escrito...', '¡Sabia decisión!', '¡Excelente!', '¡Correcto!'] }
];

// --- DATOS DE LA AVENTURA (GÉNESIS) ---
const CHAPTERS = [
    {
        title: "Capítulo 1: La Creación 🌍",
        story: "¡Hola constructor! Al principio todo estaba desordenado. Dios decidió crear un mundo hermoso. ¿Nos ayudas a poner cada bloque en su lugar para formar la Creación?",
        goal: 300,
        scripture: "“En el principio creó Dios los cielos y la tierra.” — Génesis 1:1",
        btnText: "¡A construir!"
    },
    {
        title: "Capítulo 2: El Jardín 🌳",
        story: "Dios creó un jardín maravilloso lleno de vida. Ahora debemos cuidarlo y mantenerlo hermoso. ¡Seamos buenos jardineros!",
        goal: 600,
        scripture: "“Tomó, pues, Dios al hombre, y lo puso en el huerto de Edén, para que lo cuidara.” — Génesis 2:15",
        btnText: "¡A cuidar!"
    },
    {
        title: "Capítulo 3: El Arca 🦁",
        story: "¡Va a llover mucho! Noé necesita nuestra ayuda para acomodar a todos los animales dentro del arca. ¡Hagamos espacio para que quepan todos!",
        goal: 1000,
        scripture: "“Y de todo lo que vive, dos de cada especie meterás en el arca.” — Génesis 6:19",
        btnText: "¡A salvar!"
    },
    {
        title: "Capítulo 4: Las Estrellas ✨",
        story: "Mira al cielo. Dios le prometió a Abraham una familia tan grande como las estrellas. ¡Sigamos construyendo esta gran historia!",
        goal: 1500,
        scripture: "“Mira ahora los cielos, y cuenta las estrellas...” — Génesis 15:5",
        btnText: "¡A soñar!"
    }
];

// Variables de interacción
let dragPiece = null; // Datos de la pieza arrastrada
let dragGhost = null; // Elemento visual flotante (canvas DOM)
let mousePos = { x: 0, y: 0 };
let isGameOver = false;
let isPaused = false; // Para pausar mientras leemos la historia

// --- FUNCIONES CORE (LÓGICA) ---

// Crea una matriz vacía para el tablero (w: ancho, h: alto)
function createMatrix(w, h) {
    const matrix = [];
    while (h--) {
        matrix.push(new Array(w).fill(0));
    }
    return matrix;
}

// El tablero de juego (12 de ancho x 20 de alto)
const arena = createMatrix(BOARD_W, BOARD_H);

// Detecta colisiones entre la pieza (player) y el tablero (arena)
function collide(arena, matrix, pos) {
    const [m, o] = [matrix, pos];
    for (let y = 0; y < m.length; ++y) {
        for (let x = 0; x < m[y].length; ++x) {
            // Verificamos si el bloque de la pieza no es 0 (aire)
            // Y si en esa posición el tablero (arena) tiene algo o es borde
            if (m[y][x] !== 0 &&
               (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0) {
                return true;
            }
        }
    }
    return false;
}

// Dibuja la matriz en el canvas (usado para tablero y pieza)
function drawMatrix(matrix, offset, ctx) {
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                const bx = x + offset.x;
                const by = y + offset.y;

                // 1. Fondo del bloque (Color suave)
                ctx.fillStyle = COLORS[value];
                
                // Usamos roundRect para bordes suaves (estilo juguete)
                ctx.beginPath();
                if (ctx.roundRect) {
                    ctx.roundRect(bx + 0.05, by + 0.05, 0.9, 0.9, 0.2);
                } else {
                    ctx.rect(bx + 0.05, by + 0.05, 0.9, 0.9); // Fallback
                }
                ctx.fill();

                // 2. Icono Vectorial (Blanco semitransparente)
                if (ICONS[value]) {
                    ctx.save();
                    ctx.translate(bx + 0.2, by + 0.2); // Centrar en el bloque
                    ctx.scale(0.6 / 24, 0.6 / 24); // Escalar path de 24px a 0.6 unidades
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
                    ctx.fill(new Path2D(ICONS[value]));
                    ctx.restore();
                }
            }
        });
    });
}

// Función principal de dibujo
function draw() {
    // Limpiar pantalla (color negro)
    boardCtx.fillStyle = '#000';
    boardCtx.fillRect(0, 0, boardCanvas.width, boardCanvas.height);

    // 1. Dibujar Tablero (Fondo y Bloques)
    // Dibujamos un fondo gris para la grilla vacía
    boardCtx.fillStyle = 'rgba(0, 0, 0, 0.2)'; // Fondo semitransparente
    boardCtx.fillRect(0, 0, BOARD_W, BOARD_H);
    drawMatrix(arena, BOARD_OFFSET, boardCtx);

    // 2. Dibujar Inventario (Piezas disponibles)
    player.inventory.forEach((p, i) => {
        const ctx = pieceContexts[i];
        // Limpiar mini canvas
        ctx.clearRect(0, 0, 4, 4); // 4x4 es el tamaño maximo en bloques
        
        if (!p.used && (!dragPiece || dragPiece.index !== i)) {
            // Centrar pieza en el mini canvas (aprox)
            const offsetX = (4 - p.matrix[0].length) / 2;
            const offsetY = (4 - p.matrix.length) / 2;
            drawMatrix(p.matrix, {x: offsetX, y: offsetY}, ctx);
        }
    });
}

// Integra la pieza al tablero cuando toca fondo
function merge(arena, matrix, pos) {
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                arena[y + pos.y][x + pos.x] = value;
            }
        });
    });
}

// Lógica de eliminación de líneas (Filas Y Columnas)
function arenaSweep() {
    let linesCleared = 0;
    const rowsToClear = [];
    const colsToClear = [];

    // 1. Identificar filas completas
    for (let y = 0; y < BOARD_H; y++) {
        if (arena[y].every(value => value !== 0)) {
            rowsToClear.push(y);
        }
    }

    // 2. Identificar columnas completas
    for (let x = 0; x < BOARD_W; x++) {
        let colFull = true;
        for (let y = 0; y < BOARD_H; y++) {
            if (arena[y][x] === 0) {
                colFull = false;
                break;
            }
        }
        if (colFull) colsToClear.push(x);
    }

    // 3. Limpiar y Puntuar
    if (rowsToClear.length > 0 || colsToClear.length > 0) {
        rowsToClear.forEach(y => arena[y].fill(0));
        colsToClear.forEach(x => {
            for(let y=0; y<BOARD_H; y++) arena[y][x] = 0;
        });

        linesCleared = rowsToClear.length + colsToClear.length;
        // Puntaje exponencial: 10, 30, 60...
        player.score += linesCleared * 10 * linesCleared; 
        showCompanionMessage('success'); // Celebrar
        
        // ESCALABILIDAD: Sonido de explosión aquí
    }

    updateScore();
}

// Genera 3 nuevas piezas si el inventario está vacío
function refillInventory() {
    const pieceTypes = '123ILJOTSZ9';
    player.inventory = [];
    for(let i=0; i<3; i++) {
        const type = pieceTypes[Math.floor(Math.random() * pieceTypes.length)];
        player.inventory.push({
            matrix: createPiece(type),
            used: false
        });
    }
    checkGameOver();
}

// Verifica si alguna pieza del inventario cabe en el tablero
function checkGameOver() {
    let canMove = false;
    
    // Revisar cada pieza disponible
    for (let p of player.inventory) {
        if (p.used) continue;
        
        // Probar en CADA posición del tablero
        for (let y = 0; y < BOARD_H; y++) {
            for (let x = 0; x < BOARD_W; x++) {
                if (!collide(arena, p.matrix, {x, y})) {
                    canMove = true;
                    break;
                }
            }
            if (canMove) break;
        }
        if (canMove) break;
    }

    if (!canMove) {
        isGameOver = true;
        isPaused = true;
        showCompanionMessage('encourage'); // Animar
        // Mostrar Modal en lugar de alert
        document.getElementById('modal-title').innerText = "¡Buen intento! 🌟";
        document.getElementById('modal-message').innerText = "Conseguiste " + player.score + " puntos.";
        document.getElementById('game-modal').classList.remove('hidden');
    }
}

// Generador de matrices de piezas
function createPiece(type) {
    if (PIECES[type]) return PIECES[type];
    if (type === 'I') return PIECES['I'];
    return PIECES['O']; // Fallback
}

function updateScore() {
    document.getElementById('score').innerText = player.score;
    
    // Verificar meta del capítulo actual
    const currentChapter = CHAPTERS[player.chapterIndex];
    if (currentChapter && player.score >= currentChapter.goal) {
        completeChapter();
    }
}

// Inicia un capítulo mostrando la historia
function startChapter(index) {
    if (index >= CHAPTERS.length) {
        alert("¡Felicidades! Has completado todas las aventuras disponibles.");
        index = 0;
        player.score = 0;
    }
    
    player.chapterIndex = index;
    const chapter = CHAPTERS[index];
    
    // Actualizar UI
    document.getElementById('level').innerText = index + 1;
    
    // Mostrar Modal de Historia
    isPaused = true;
    document.getElementById('story-title').innerText = chapter.title.replace("Capítulo", "Cap.");
    document.getElementById('story-text').innerText = chapter.story;
    document.getElementById('start-chapter-btn').innerText = chapter.btnText;
    document.getElementById('story-modal').classList.remove('hidden');
}

function completeChapter() {
    isPaused = true;
    const chapter = CHAPTERS[player.chapterIndex];
    
    document.getElementById('modal-title').innerText = "¡Capítulo Completado! 🎉";
    document.getElementById('modal-message').innerText = chapter.scripture;
    
    const btn = document.getElementById('action-btn');
    btn.innerText = "Siguiente Aventura ➡️";
    btn.onclick = () => {
        document.getElementById('game-modal').classList.add('hidden');
        startChapter(player.chapterIndex + 1);
    };
    
    document.getElementById('game-modal').classList.remove('hidden');
}

// --- BUCLE PRINCIPAL (GAME LOOP) ---

function update(time = 0) {
    // Solo dibujamos, la lógica es por eventos
    draw();
    requestAnimationFrame(update);
}

// --- CONTROLES (MOUSE) ---

// Función auxiliar para obtener coordenadas (Mouse o Touch)
function getEventPos(e) {
    if (e.touches && e.touches.length > 0) {
        return { x: e.touches[0].clientX, y: e.touches[0].clientY };
    }
    return { x: e.clientX, y: e.clientY };
}

// Eventos para cada mini-canvas de pieza
pieceCanvases.forEach((canvas, index) => {
    // Manejador unificado para iniciar arrastre
    const handleStart = (e) => {
        if (isGameOver || isPaused || player.inventory[index].used) return;
        if (e.type === 'touchstart') e.preventDefault(); // Evitar scroll

        const p = player.inventory[index];
        
        // 1. Crear elemento fantasma (Ghost)
        dragGhost = document.createElement('canvas');
        dragGhost.width = p.matrix[0].length * BLOCK_SIZE;
        dragGhost.height = p.matrix.length * BLOCK_SIZE;
        const gCtx = dragGhost.getContext('2d');
        gCtx.scale(BLOCK_SIZE, BLOCK_SIZE);
        drawMatrix(p.matrix, {x:0, y:0}, gCtx);

        // Estilos del fantasma
        dragGhost.style.position = 'fixed';
        dragGhost.style.pointerEvents = 'none'; // Importante para que el mouseup pase a través
        dragGhost.style.zIndex = '1000';
        dragGhost.style.opacity = '0.9';
        dragGhost.style.transform = 'translate(-50%, -50%)'; // Centrar en el mouse
        
        document.body.appendChild(dragGhost);

        // 2. Iniciar estado de arrastre
        dragPiece = { 
            index: index,
            matrix: p.matrix
        };

        // Posicionar inicialmente
        const pos = getEventPos(e);
        updateGhostPosition(pos.x, pos.y);
    };

    canvas.addEventListener('mousedown', handleStart);
    canvas.addEventListener('touchstart', handleStart, { passive: false });
});

// Eventos globales para mover el fantasma y soltar
const handleMove = (e) => {
    if (!dragPiece) return;
    if (e.type === 'touchmove') e.preventDefault(); // Evitar scroll

    const pos = getEventPos(e);
    updateGhostPosition(pos.x, pos.y);

    // Calcular posición relativa al tablero para lógica de juego
    const rect = boardCanvas.getBoundingClientRect();
    const scaleX = boardCanvas.width / rect.width;
    const scaleY = boardCanvas.height / rect.height;

    // Ajustamos para que el centro de la pieza sea el puntero
    const pieceW = dragPiece.matrix[0].length * BLOCK_SIZE;
    const pieceH = dragPiece.matrix.length * BLOCK_SIZE;

    // Coordenada en el canvas (centrada en el mouse)
    const canvasX = (pos.x - rect.left) * scaleX - (pieceW / 2);
    const canvasY = (pos.y - rect.top) * scaleY - (pieceH / 2);

    mousePos.x = canvasX / BLOCK_SIZE;
    mousePos.y = canvasY / BLOCK_SIZE;
};

const handleEnd = (e) => {
    if (!dragPiece) return;

    // Limpiar fantasma
    if (dragGhost) {
        dragGhost.remove();
        dragGhost = null;
    }

    // Calcular posición de grilla (redondeo simple)
    const boardX = Math.round(mousePos.x);
    const boardY = Math.round(mousePos.y);

    const p = player.inventory[dragPiece.index];

    // Intentar colocar
    if (!collide(arena, p.matrix, {x: boardX, y: boardY})) {
        // Éxito: Colocar pieza
        merge(arena, p.matrix, {x: boardX, y: boardY});
        p.used = true;
        player.score += 10; // Puntos por colocar
        
        arenaSweep(); // Limpiar líneas

        // Si se usaron todas, rellenar
        if (player.inventory.every(p => p.used)) {
            refillInventory();
        } else {
            checkGameOver(); // Verificar si quedan movimientos con las piezas restantes
        }
    }

    dragPiece = null;
};

window.addEventListener('mousemove', handleMove);
window.addEventListener('touchmove', handleMove, { passive: false });

window.addEventListener('mouseup', handleEnd);
window.addEventListener('touchend', handleEnd);

function updateGhostPosition(x, y) {
    if (dragGhost) {
        dragGhost.style.left = x + 'px';
        dragGhost.style.top = y + 'px';
    }
}

// --- LÓGICA DE PERSONALIZACIÓN Y MENSAJES ---

function initSetup() {
    // Llenar grilla de personajes
    const grid = document.getElementById('char-selection');
    grid.innerHTML = '';
    CHARACTERS.forEach(char => {
        const div = document.createElement('div');
        div.className = 'char-card';
        div.innerHTML = `<span class="char-icon">${char.icon}</span><span class="char-name">${char.name}</span>`;
        div.onclick = () => selectCharacter(char.id, div);
        grid.appendChild(div);
    });
    
    // Seleccionar el primero por defecto visualmente
    selectCharacter('sheep', grid.firstChild);
}

function selectCharacter(id, element) {
    playerData.characterId = id;
    // Actualizar visualmente la selección
    document.querySelectorAll('.char-card').forEach(el => el.classList.remove('selected'));
    if(element) element.classList.add('selected');
}

function showCompanionMessage(type) {
    const char = CHARACTERS.find(c => c.id === playerData.characterId) || CHARACTERS[0];
    const bubble = document.getElementById('comp-msg');
    const avatar = document.getElementById('comp-avatar');
    
    let text = "";
    
    if (type === 'success') {
        // Mensaje aleatorio del personaje
        text = char.msgs[Math.floor(Math.random() * char.msgs.length)];
        // 30% de probabilidad de usar el nombre
        if (Math.random() > 0.7) text += `, ${playerData.name}!`;
    } else if (type === 'encourage') {
        text = `¡No te rindas, ${playerData.name}!`;
    } else if (type === 'welcome') {
        text = `¡Vamos, ${playerData.name}!`;
    }

    // Mostrar
    avatar.innerText = char.icon;
    bubble.innerText = text;
    bubble.style.opacity = '1';
    
    // Ocultar después de 3 segundos
    setTimeout(() => {
        bubble.style.opacity = '0';
    }, 3000);
}

// --- FLUJO DE INICIO ---

document.getElementById('next-step-btn').addEventListener('click', () => {
    const input = document.getElementById('player-name-input');
    if (input.value.trim() !== "") {
        playerData.name = input.value.trim();
        document.getElementById('step-name').classList.add('hidden');
        document.getElementById('step-char').classList.remove('hidden');
        initSetup(); // Inicializar grilla si no estaba
    }
});

// Crear botón final para comenzar juego desde selección de personaje
const startBtn = document.createElement('button');
startBtn.className = 'btn-primary';
startBtn.innerText = '¡Comenzar Aventura! 🚀';
startBtn.style.marginTop = '20px';
startBtn.onclick = () => {
    document.getElementById('setup-modal').classList.add('hidden');
    document.getElementById('companion-area').classList.remove('hidden');
    showCompanionMessage('welcome');
    startChapter(0);
};
document.getElementById('step-char').appendChild(startBtn);

// --- EVENTOS UI ---

// Botón para cerrar historia y empezar a jugar
document.getElementById('start-chapter-btn').addEventListener('click', () => {
    document.getElementById('story-modal').classList.add('hidden');
    isPaused = false;
});

// Botón del modal principal (Game Over o Completado)
document.getElementById('action-btn').addEventListener('click', () => {
    // Si es Game Over, reiniciamos el capítulo actual
    if (isGameOver) {
        document.getElementById('game-modal').classList.add('hidden');
        arena.forEach(row => row.fill(0));
        player.score = 0; // Opcional: resetear score o mantenerlo
        isGameOver = false;
        isPaused = false;
        refillInventory();
        updateScore();
        startChapter(player.chapterIndex); // Re-mostrar historia
    }
});

// INICIO
refillInventory(); // Preparar piezas
updateScore(); // Resetear score visual
// startChapter(0); // YA NO INICIAMOS DIRECTO, ESPERAMOS AL SETUP
update();