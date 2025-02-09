import java.io.*;
import java.net.*;

// TicTacToeServer: Kelas ini merepresentasikan server untuk permainan Tic Tac Toe
public class TicTacToeServer {
    private static char[] board = new char[9]; // Papan permainan Tic Tac Toe, berisi 9 sel
    private static int moveCount = 0; // Jumlah total gerakan yang telah dilakukan

    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(12345); // Membuka server socket pada port 12345
        System.out.println("Server is running on port 12345...");

        // Inisialisasi papan dengan karakter kosong
        for (int i = 0; i < 9; i++) board[i] = ' ';

        // Menunggu koneksi dari dua pemain
        Socket player1 = serverSocket.accept(); // Menerima koneksi dari Player 1
        System.out.println("Player 1 connected (X)");
        Socket player2 = serverSocket.accept(); // Menerima koneksi dari Player 2
        System.out.println("Player 2 connected (O)");

        // Stream untuk komunikasi antara server dan pemain
        DataOutputStream toPlayer1 = new DataOutputStream(player1.getOutputStream());
        DataOutputStream toPlayer2 = new DataOutputStream(player2.getOutputStream());
        DataInputStream fromPlayer1 = new DataInputStream(player1.getInputStream());
        DataInputStream fromPlayer2 = new DataInputStream(player2.getInputStream());

        // Beri tanda ke masing-masing pemain
        toPlayer1.writeUTF("X"); // Player 1 akan menggunakan tanda X
        toPlayer2.writeUTF("O"); // Player 2 akan menggunakan tanda O

        boolean running = true; // Menandai apakah permainan masih berjalan

        while (running) {
            // Giliran Player 1
            toPlayer1.writeUTF("YOUR_MOVE"); // Instruksi kepada Player 1 untuk bergerak
            int move1 = Integer.parseInt(fromPlayer1.readUTF()); // Terima gerakan Player 1
            board[move1] = 'X'; // Tandai papan dengan tanda X
            moveCount++; // Tambah jumlah gerakan

            // Periksa apakah Player 1 menang
            if (checkWin('X')) {
                toPlayer1.writeUTF("WIN"); // Beritahu Player 1 menang
                toPlayer2.writeUTF("LOSE"); // Beritahu Player 2 kalah
                running = false; // Hentikan permainan
                break;
            }

            // Periksa apakah permainan berakhir dengan seri
            if (moveCount == 9) {
                toPlayer1.writeUTF("DRAW"); // Beritahu kedua pemain bahwa permainan seri
                toPlayer2.writeUTF("DRAW");
                running = false; // Hentikan permainan
                break;
            }

            toPlayer2.writeUTF(String.valueOf(move1)); // Kirim gerakan Player 1 ke Player 2

            // Giliran Player 2
            toPlayer2.writeUTF("YOUR_MOVE"); // Instruksi kepada Player 2 untuk bergerak
            int move2 = Integer.parseInt(fromPlayer2.readUTF()); // Terima gerakan Player 2
            board[move2] = 'O'; // Tandai papan dengan tanda O
            moveCount++; // Tambah jumlah gerakan

            // Periksa apakah Player 2 menang
            if (checkWin('O')) {
                toPlayer2.writeUTF("WIN"); // Beritahu Player 2 menang
                toPlayer1.writeUTF("LOSE"); // Beritahu Player 1 kalah
                running = false; // Hentikan permainan
                break;
            }

            // Periksa apakah permainan berakhir dengan seri
            if (moveCount == 9) {
                toPlayer1.writeUTF("DRAW"); // Beritahu kedua pemain bahwa permainan seri
                toPlayer2.writeUTF("DRAW");
                running = false; // Hentikan permainan
                break;
            }

            toPlayer1.writeUTF(String.valueOf(move2)); // Kirim gerakan Player 2 ke Player 1
        }

        System.out.println("Game Over!"); // Tampilkan pesan akhir permainan di server

        // Tutup koneksi
        player1.close();
        player2.close();
        serverSocket.close();
    }

    // Metode untuk memeriksa apakah pemain tertentu menang
    private static boolean checkWin(char mark) {
        int[][] winPatterns = {
                {0, 1, 2}, {3, 4, 5}, {6, 7, 8}, // Pola kemenangan baris
                {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, // Pola kemenangan kolom
                {0, 4, 8}, {2, 4, 6}  // Pola kemenangan diagonal
        };
        // Periksa setiap pola kemenangan
        for (int[] pattern : winPatterns) {
            if (board[pattern[0]] == mark && board[pattern[1]] == mark && board[pattern[2]] == mark) {
                return true; // Jika pola terpenuhi, pemain menang
            }
        }
        return false; // Tidak ada pola kemenangan
    }
}
