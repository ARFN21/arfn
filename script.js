const books = [
  { title: 'Langit Senja', author: 'Ayu Larasati', genre: 'Fiksi', year: 2021, status: 'available' },
  { title: 'Jejak Bumi', author: 'Bima Prasetyo', genre: 'Petualangan', year: 2019, status: 'checked-out' },
  { title: 'Arus Tengah', author: 'Citra Dewi', genre: 'Fiksi', year: 2020, status: 'available' },
  { title: 'Warna Pagi', author: 'Dewi Kinasih', genre: 'Romansa', year: 2022, status: 'available' },
  { title: 'Lautan Kata', author: 'Eko Firmansyah', genre: 'Puisi', year: 2018, status: 'checked-out' },
  { title: 'Misi Antariksa', author: 'Farhan Ramdani', genre: 'Sci-Fi', year: 2023, status: 'available' },
  { title: 'Gelombang Sunyi', author: 'Gita Permata', genre: 'Drama', year: 2017, status: 'available' },
  { title: 'Kota Tua', author: 'Hariyanto', genre: 'Sejarah', year: 2016, status: 'checked-out' },
  { title: 'Sisi Lain Hutan', author: 'Indra Mahardika', genre: 'Petualangan', year: 2020, status: 'available' },
  { title: 'Bulan Purnama', author: 'Jihan Rahma', genre: 'Romansa', year: 2021, status: 'available' },
  { title: 'Ruang Tanpa Batas', author: 'Kamal Wijaya', genre: 'Sci-Fi', year: 2019, status: 'checked-out' },
  { title: 'Bumi Nan Jauh', author: 'Lestari Putri', genre: 'Fiksi', year: 2022, status: 'available' },
  { title: 'Matahari Biru', author: 'Mira Andini', genre: 'Sci-Fi', year: 2018, status: 'available' },
  { title: 'Jendela Kayu', author: 'Niko Saputra', genre: 'Drama', year: 2015, status: 'checked-out' },
  { title: 'Rasa Laut', author: 'Oka Pradana', genre: 'Puisi', year: 2017, status: 'available' },
  { title: 'Garis Waktu', author: 'Putri Anindya', genre: 'Romansa', year: 2019, status: 'available' },
  { title: 'Semburat Asa', author: 'Qori Annisa', genre: 'Puisi', year: 2020, status: 'checked-out' },
  { title: 'Kisah Tiga Kota', author: 'Rama Surya', genre: 'Sejarah', year: 2016, status: 'available' },
  { title: 'Bentang Langit', author: 'Sari Utami', genre: 'Fiksi', year: 2023, status: 'available' },
  { title: 'Jejak Ombak', author: 'Tara Wulandari', genre: 'Petualangan', year: 2018, status: 'checked-out' },
  { title: 'Rindu Senandung', author: 'Umar Faruq', genre: 'Romansa', year: 2021, status: 'available' },
  { title: 'Titik Balik', author: 'Vina Prameswari', genre: 'Drama', year: 2022, status: 'available' },
  { title: 'Rumah di Lereng', author: 'Wahyu Aditya', genre: 'Fiksi', year: 2017, status: 'checked-out' },
  { title: 'Langkah Kecil', author: 'Xena Kartika', genre: 'Motivasi', year: 2020, status: 'available' },
  { title: 'Jalur Timur', author: 'Yoga Darma', genre: 'Petualangan', year: 2019, status: 'checked-out' },
  { title: 'Cahaya Kota', author: 'Zahra Azzahra', genre: 'Drama', year: 2018, status: 'available' },
  { title: 'Dunia Dalam Kata', author: 'Arman Wirawan', genre: 'Puisi', year: 2016, status: 'available' },
  { title: 'Pengembaraan Utara', author: 'Bela Anggraini', genre: 'Petualangan', year: 2022, status: 'available' },
  { title: 'Racikan Rasa', author: 'Cici Rahmadani', genre: 'Kuliner', year: 2021, status: 'checked-out' },
  { title: 'Taman Rahasia', author: 'Dian Febriana', genre: 'Fiksi', year: 2019, status: 'available' },
  { title: 'Nada-Nada Pagi', author: 'Erlangga Pradipta', genre: 'Puisi', year: 2023, status: 'available' },
  { title: 'Merawat Kota', author: 'Fadli Prasetya', genre: 'Sejarah', year: 2018, status: 'available' },
  { title: 'Berkah Musim', author: 'Gilang Prakoso', genre: 'Nonfiksi', year: 2020, status: 'checked-out' },
  { title: 'Jalur Rahasia', author: 'Hana Cahyani', genre: 'Petualangan', year: 2021, status: 'available' },
  { title: 'Titik Cahaya', author: 'Intan Melati', genre: 'Romansa', year: 2017, status: 'available' },
  { title: 'Waktu Berjalan', author: 'Jordi Kurnia', genre: 'Drama', year: 2022, status: 'checked-out' },
  { title: 'Pelangi Timur', author: 'Kania Dewantara', genre: 'Fiksi', year: 2023, status: 'available' },
  { title: 'Harmoni Rasa', author: 'Laras Yunita', genre: 'Kuliner', year: 2016, status: 'available' },
  { title: 'Cerita Utama', author: 'Made Wirya', genre: 'Fiksi', year: 2019, status: 'available' },
  { title: 'Sebuah Jalan', author: 'Nadya Laksmi', genre: 'Motivasi', year: 2020, status: 'checked-out' },
  { title: 'Detak Kota', author: 'Omar Rizky', genre: 'Sejarah', year: 2017, status: 'available' },
  { title: 'Pada Musim Hujan', author: 'Prita Cahaya', genre: 'Drama', year: 2018, status: 'available' },
  { title: 'Setapak Pagi', author: 'Qomaruddin', genre: 'Motivasi', year: 2021, status: 'available' },
  { title: 'Lintas Cakrawala', author: 'Rizal Ramadhan', genre: 'Sci-Fi', year: 2020, status: 'checked-out' },
  { title: 'Lukisan Sunyi', author: 'Syifa Maulida', genre: 'Romansa', year: 2019, status: 'available' },
  { title: 'Resonansi Waktu', author: 'Tegar Wiratma', genre: 'Sci-Fi', year: 2022, status: 'available' },
  { title: 'Hening Siang', author: 'Unun Safitri', genre: 'Puisi', year: 2016, status: 'checked-out' },
  { title: 'Malam Terang', author: 'Vivi Anindita', genre: 'Drama', year: 2023, status: 'available' },
  { title: 'Pijakan Awan', author: 'Wildan Kusuma', genre: 'Fiksi', year: 2017, status: 'available' },
  { title: 'Jejak Cahaya', author: 'Yuni Astuti', genre: 'Romansa', year: 2018, status: 'available' },
  { title: 'Ruang Hening', author: 'Zidan Maulana', genre: 'Nonfiksi', year: 2021, status: 'checked-out' },
];

const elements = {
  grid: document.getElementById('book-grid'),
  search: document.getElementById('search'),
  genre: document.getElementById('genre'),
  sort: document.getElementById('sort'),
  availability: document.getElementById('availability'),
  reset: document.getElementById('reset-filters'),
  favoritesToggle: document.getElementById('toggle-favorites'),
  favoritesInfo: document.getElementById('favorites-info'),
  clearFavorites: document.getElementById('clear-favorites'),
  toggleTheme: document.getElementById('toggle-theme'),
};

let favorites = new Set(JSON.parse(localStorage.getItem('favorites') || '[]'));
let showFavoritesOnly = false;

const uniqueGenres = Array.from(new Set(books.map((b) => b.genre))).sort();
uniqueGenres.forEach((genre) => {
  const option = document.createElement('option');
  option.value = genre;
  option.textContent = genre;
  elements.genre.appendChild(option);
});

function renderBooks() {
  elements.grid.innerHTML = '';

  const query = elements.search.value.toLowerCase();
  const selectedGenre = elements.genre.value;
  const selectedAvailability = elements.availability.value;

  let filtered = books.filter((book) => {
    const matchesQuery = book.title.toLowerCase().includes(query) ||
      book.author.toLowerCase().includes(query);
    const matchesGenre = !selectedGenre || book.genre === selectedGenre;
    const matchesAvailability = !selectedAvailability || book.status === selectedAvailability;
    const matchesFavorite = !showFavoritesOnly || favorites.has(book.title);
    return matchesQuery && matchesGenre && matchesAvailability && matchesFavorite;
  });

  const sortMode = elements.sort.value;
  filtered.sort((a, b) => {
    if (sortMode === 'title') return a.title.localeCompare(b.title);
    if (sortMode === 'author') return a.author.localeCompare(b.author);
    if (sortMode === 'year-desc') return b.year - a.year;
    return 0;
  });

  if (filtered.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'card';
    empty.innerHTML = '<p class="eyebrow">Hasil kosong</p><h3>Tidak ada buku yang cocok.</h3>';
    elements.grid.appendChild(empty);
    return;
  }

  const template = document.getElementById('book-card-template');

  filtered.forEach((book) => {
    const node = template.content.cloneNode(true);
    const card = node.querySelector('.card');
    card.querySelector('.title').textContent = book.title;
    card.querySelector('.author').textContent = book.author;
    card.querySelector('.genre').textContent = book.genre;
    card.querySelector('.year').textContent = book.year;

    const statusEl = card.querySelector('.status');
    statusEl.textContent = book.status === 'available' ? 'Tersedia' : 'Dipinjam';
    statusEl.classList.add(book.status);

    const favBtn = card.querySelector('.favorite');
    const isFavorite = favorites.has(book.title);
    favBtn.textContent = isFavorite ? '⭐' : '☆';
    favBtn.classList.toggle('is-favorite', isFavorite);
    favBtn.addEventListener('click', () => toggleFavorite(book.title, favBtn));

    elements.grid.appendChild(node);
  });
}

function toggleFavorite(title, button) {
  if (favorites.has(title)) {
    favorites.delete(title);
  } else {
    favorites.add(title);
  }
  localStorage.setItem('favorites', JSON.stringify(Array.from(favorites)));
  if (button) {
    button.textContent = favorites.has(title) ? '⭐' : '☆';
    button.classList.toggle('is-favorite');
  }
  updateFavoritesChip();
  renderBooks();
}

function resetFilters() {
  elements.search.value = '';
  elements.genre.value = '';
  elements.availability.value = '';
  elements.sort.value = 'title';
  showFavoritesOnly = false;
  updateFavoritesChip();
  renderBooks();
}

function updateFavoritesChip() {
  elements.favoritesInfo.hidden = !showFavoritesOnly;
}

function initThemeToggle() {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark') document.documentElement.classList.add('dark');

  elements.toggleTheme.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    const active = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    elements.toggleTheme.textContent = active === 'dark' ? '☀️' : '🌙';
    localStorage.setItem('theme', active);
  });

  const active = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  elements.toggleTheme.textContent = active === 'dark' ? '☀️' : '🌙';
}

function bindEvents() {
  elements.search.addEventListener('input', renderBooks);
  elements.genre.addEventListener('change', renderBooks);
  elements.availability.addEventListener('change', renderBooks);
  elements.sort.addEventListener('change', renderBooks);
  elements.reset.addEventListener('click', resetFilters);

  elements.favoritesToggle.addEventListener('click', () => {
    showFavoritesOnly = !showFavoritesOnly;
    elements.favoritesToggle.textContent = showFavoritesOnly ? 'Lihat semua' : 'Lihat favorit';
    updateFavoritesChip();
    renderBooks();
  });

  elements.clearFavorites.addEventListener('click', () => {
    favorites.clear();
    localStorage.removeItem('favorites');
    renderBooks();
    updateFavoritesChip();
  });
}

function init() {
  bindEvents();
  initThemeToggle();
  renderBooks();
}

init();
