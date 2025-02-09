import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.*;

// TicTacToeClient: Kelas ini merepresentasikan klien untuk permainan Tic Tac Toe
public class TicTacToeClient extends JFrame {
    private char myMark; // X atau O untuk menandai pemain
    private boolean myTurn = false; // Menandai giliran pemain saat ini
    private JButton[] buttons = new JButton[9]; // Tombol untuk setiap sel di papan Tic Tac Toe
    private DataOutputStream toServer; // Stream untuk mengirim data ke server
    private DataInputStream fromServer; // Stream untuk menerima data dari server

    // Konstruktor klien Tic Tac Toe
    public TicTacToeClient(String serverAddress) {
        setTitle("Tic Tac Toe");
        setSize(400, 400);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new GridLayout(3, 3)); // Atur layout grid 3x3 untuk papan permainan

        // Inisialisasi tombol papan permainan
        for (int i = 0; i < 9; i++) {
            buttons[i] = new JButton(""); // Tombol awal tanpa teks
            buttons[i].setFont(new Font("Arial", Font.PLAIN, 40)); // Atur font tombol
            buttons[i].setFocusPainted(false); // Hilangkan efek fokus pada tombol
            buttons[i].addActionListener(new ButtonListener(i)); // Tambahkan event listener ke tombol
            buttons[i].setEnabled(false); // Nonaktifkan tombol di awal
            add(buttons[i]); // Tambahkan tombol ke framello
        }

        try {
            // Koneksi ke server
            Socket socket = new Socket(serverAddress, 12345);
            fromServer = new DataInputStream(socket.getInputStream()); // Input dari server
            toServer = new DataOutputStream(socket.getOutputStream()); // Output ke server

            // Terima tanda pemain dari server (X atau O)
            myMark = fromServer.readUTF().charAt(0);
            setTitle("Tic Tac Toe - You are " + myMark); // Perbarui judul dengan tanda pemain

            // Jalankan thread untuk mendengarkan pesan dari server
            new Thread(() -> {
                try {
                    while (true) {
                        String response = fromServer.readUTF(); // Baca pesan dari server

                        if (response.equals("YOUR_MOVE")) { // Giliran pemain
                            myTurn = true;
                            enableEmptyButtons(); // Aktifkan tombol kosong
                        } else if (response.equals("WIN") || response.equals("LOSE") || response.equals("DRAW")) { // Akhir permainan
                            JOptionPane.showMessageDialog(this, response); // Tampilkan hasil permainan
                            disableAllButtons(); // Nonaktifkan semua tombol
                            break; // Keluar dari loop
                        } else { // Gerakan lawan
                            int index = Integer.parseInt(response); // Terima indeks gerakan lawan
                            buttons[index].setText(myMark == 'X' ? "O" : "X"); // Tandai tombol dengan tanda lawan
                            buttons[index].setEnabled(false); // Nonaktifkan tombol tersebut
                        }
                    }
                } catch (IOException ex) {
                    ex.printStackTrace(); // Tangani error input/output
                }
            }).start();

        } catch (IOException ex) {
            ex.printStackTrace(); // Tangani error saat mencoba koneksi
        }
    }

    // Inner class untuk menangani event klik tombol
    private class ButtonListener implements ActionListener {
        private int index; // Indeks tombol

        public ButtonListener(int index) {
            this.index = index; // Simpan indeks tombol yang diklik
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            if (myTurn && buttons[index].getText().equals("")) { // Pastikan tombol kosong dan giliran pemain
                buttons[index].setText(String.valueOf(myMark)); // Tandai tombol dengan tanda pemain
                buttons[index].setEnabled(false); // Nonaktifkan tombol setelah digunakan
                myTurn = false; // Ganti giliran pemain
                disableAllButtons(); // Nonaktifkan semua tombol
                try {
                    toServer.writeUTF(String.valueOf(index)); // Kirim indeks gerakan ke server
                } catch (IOException ex) {
                    ex.printStackTrace(); // Tangani error input/output
                }
            }
        }
    }

    // Aktifkan tombol kosong untuk gerakan
    private void enableEmptyButtons() {
        for (JButton button : buttons) {
            if (button.getText().equals("")) {
                button.setEnabled(true); // Aktifkan tombol jika kosong
            }
        }
    }

    // Nonaktifkan semua tombol
    private void disableAllButtons() {
        for (JButton button : buttons) {
            button.setEnabled(false); // Nonaktifkan tombol
        }
    }

    // Metode utama untuk menjalankan program
    public static void main(String[] args) {
        String serverAddress = JOptionPane.showInputDialog("Alamat lawan:"); // Minta alamat server dari pengguna
        if (serverAddress != null) { // Pastikan alamat server tidak null
            SwingUtilities.invokeLater(() -> new TicTacToeClient(serverAddress).setVisible(true)); // Jalankan GUI
        }
    }
}
