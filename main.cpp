#include <algorithm>
#include <cctype>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

struct Book {
    int id{};
    std::string title;
    std::string author;
    int year{};
    std::string genre;
    bool available{true};
};

std::string toLower(std::string text) {
    std::transform(text.begin(), text.end(), text.begin(), [](unsigned char ch) {
        return static_cast<char>(std::tolower(ch));
    });
    return text;
}

std::string trimText(const std::string &text, std::size_t width) {
    if (text.size() <= width) {
        return text;
    }
    if (width <= 3) {
        return text.substr(0, width);
    }
    return text.substr(0, width - 3) + "...";
}

bool parseBook(const std::string &line, Book &book) {
    std::stringstream ss(line);
    std::string field;
    std::vector<std::string> fields;

    while (std::getline(ss, field, ',')) {
        fields.push_back(field);
    }

    if (fields.size() != 6) {
        return false;
    }

    book.id = std::stoi(fields[0]);
    book.title = fields[1];
    book.author = fields[2];
    book.year = std::stoi(fields[3]);
    book.genre = fields[4];
    book.available = fields[5] == "available";
    return true;
}

std::vector<Book> loadBooks(const std::string &path) {
    std::vector<Book> books;
    std::ifstream file(path);
    if (!file.is_open()) {
        std::cerr << "Tidak bisa membuka file data: " << path << "\n";
        return books;
    }

    std::string line;
    bool firstLine = true;
    while (std::getline(file, line)) {
        if (firstLine) {
            firstLine = false; // skip header
            continue;
        }
        if (line.empty()) {
            continue;
        }
        Book book;
        if (parseBook(line, book)) {
            books.push_back(book);
        }
    }
    return books;
}

void saveBooks(const std::string &path, const std::vector<Book> &books) {
    std::ofstream file(path);
    file << "id,title,author,year,genre,status\n";
    for (const auto &book : books) {
        file << book.id << ',' << book.title << ',' << book.author << ',' << book.year << ','
             << book.genre << ',' << (book.available ? "available" : "borrowed") << "\n";
    }
}

void printBanner() {
    std::cout << "==============================\n";
    std::cout << "  PERPUSTAKAAN KAMPUS MODERN  \n";
    std::cout << "==============================\n\n";
}

void printTable(const std::vector<Book> &books) {
    const int idWidth = 4;
    const int titleWidth = 32;
    const int authorWidth = 18;
    const int genreWidth = 14;
    const int yearWidth = 6;
    const int statusWidth = 11;

    auto printSeparator = [&]() {
        std::cout << '+' << std::string(idWidth + 2, '-') << '+' << std::string(titleWidth + 2, '-')
                  << '+' << std::string(authorWidth + 2, '-') << '+'
                  << std::string(genreWidth + 2, '-') << '+' << std::string(yearWidth + 2, '-')
                  << '+' << std::string(statusWidth + 2, '-') << "+\n";
    };

    printSeparator();
    std::cout << "| " << std::left << std::setw(idWidth) << "ID" << " | " << std::setw(titleWidth)
              << "Judul" << " | " << std::setw(authorWidth) << "Penulis" << " | "
              << std::setw(genreWidth) << "Genre" << " | " << std::setw(yearWidth) << "Tahun" << " | "
              << std::setw(statusWidth) << "Status" << " |\n";
    printSeparator();

    for (const auto &book : books) {
        std::cout << "| " << std::left << std::setw(idWidth) << book.id << " | "
                  << std::setw(titleWidth) << trimText(book.title, titleWidth) << " | "
                  << std::setw(authorWidth) << trimText(book.author, authorWidth) << " | "
                  << std::setw(genreWidth) << trimText(book.genre, genreWidth) << " | "
                  << std::setw(yearWidth) << book.year << " | "
                  << std::setw(statusWidth) << (book.available ? "Tersedia" : "Dipinjam") << " |\n";
    }
    printSeparator();
}

void listBooks(const std::vector<Book> &books) {
    if (books.empty()) {
        std::cout << "Belum ada data buku.\n";
        return;
    }
    printTable(books);
}

void searchBooks(const std::vector<Book> &books) {
    std::cout << "Masukkan kata kunci judul/penulis: ";
    std::string query;
    std::getline(std::cin, query);
    auto loweredQuery = toLower(query);

    std::vector<Book> results;
    for (const auto &book : books) {
        auto title = toLower(book.title);
        auto author = toLower(book.author);
        if (title.find(loweredQuery) != std::string::npos ||
            author.find(loweredQuery) != std::string::npos) {
            results.push_back(book);
        }
    }

    if (results.empty()) {
        std::cout << "Tidak ada buku yang cocok dengan kata kunci.\n";
        return;
    }

    std::cout << "\nHasil pencarian:\n";
    printTable(results);
}

Book *findBook(std::vector<Book> &books, int id) {
    for (auto &book : books) {
        if (book.id == id) {
            return &book;
        }
    }
    return nullptr;
}

void borrowBook(std::vector<Book> &books) {
    std::cout << "Masukkan ID buku yang ingin dipinjam: ";
    int id;
    if (!(std::cin >> id)) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Input tidak valid.\n";
        return;
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    Book *book = findBook(books, id);
    if (!book) {
        std::cout << "ID buku tidak ditemukan.\n";
        return;
    }
    if (!book->available) {
        std::cout << "Buku sedang dipinjam. Pilih buku lain.\n";
        return;
    }

    book->available = false;
    std::cout << "Berhasil meminjam: " << book->title << "\n";
}

void returnBook(std::vector<Book> &books) {
    std::cout << "Masukkan ID buku yang ingin dikembalikan: ";
    int id;
    if (!(std::cin >> id)) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Input tidak valid.\n";
        return;
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    Book *book = findBook(books, id);
    if (!book) {
        std::cout << "ID buku tidak ditemukan.\n";
        return;
    }
    if (book->available) {
        std::cout << "Buku sudah berada di perpustakaan.\n";
        return;
    }

    book->available = true;
    std::cout << "Terima kasih, pengembalian tercatat untuk: " << book->title << "\n";
}

void showSummary(const std::vector<Book> &books) {
    int available = 0;
    int borrowed = 0;
    for (const auto &book : books) {
        if (book.available) {
            ++available;
        } else {
            ++borrowed;
        }
    }

    std::cout << "\nRingkasan koleksi:\n";
    std::cout << " - Total judul:  " << books.size() << "\n";
    std::cout << " - Tersedia:     " << available << "\n";
    std::cout << " - Dipinjam:     " << borrowed << "\n";
}

void showMenu() {
    std::cout << "\nPilih menu:\n";
    std::cout << " 1. Lihat semua buku\n";
    std::cout << " 2. Cari buku\n";
    std::cout << " 3. Pinjam buku\n";
    std::cout << " 4. Kembalikan buku\n";
    std::cout << " 5. Lihat ringkasan koleksi\n";
    std::cout << " 6. Simpan dan keluar\n";
    std::cout << "Pilihan Anda: ";
}

int main() {
    const std::string dataPath = "data/books.csv";
    std::vector<Book> books = loadBooks(dataPath);
    if (books.empty()) {
        std::cout << "Tidak ada data buku untuk ditampilkan. Pastikan data/books.csv tersedia.\n";
        return 1;
    }

    printBanner();
    bool running = true;
    while (running) {
        showMenu();
        std::string choice;
        std::getline(std::cin, choice);

        if (choice == "1") {
            listBooks(books);
        } else if (choice == "2") {
            searchBooks(books);
        } else if (choice == "3") {
            borrowBook(books);
        } else if (choice == "4") {
            returnBook(books);
        } else if (choice == "5") {
            showSummary(books);
        } else if (choice == "6") {
            saveBooks(dataPath, books);
            running = false;
            std::cout << "Perubahan disimpan. Sampai jumpa!\n";
        } else {
            std::cout << "Pilihan tidak dikenali. Silakan pilih 1-6.\n";
        }
    }
    return 0;
}
