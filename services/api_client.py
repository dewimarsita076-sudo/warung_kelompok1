"""
Client REST API untuk mengambil kurs mata uang asing.
"""

import requests


BASE_URL = "https://api.frankfurter.app"
REQUEST_TIMEOUT = 10


def get_kurs(mata_uang_tujuan: str) -> float:
    """
    Mengambil kurs terbaru dari IDR menuju mata uang tujuan.

    Args:
        mata_uang_tujuan:
            Kode mata uang, misalnya USD, JPY, EUR, atau SGD.

    Returns:
        Nilai kurs sebagai float.

    Raises:
        ValueError:
            Jika mata uang tidak valid atau respons API bermasalah.

        ConnectionError:
            Jika terjadi timeout atau koneksi internet bermasalah.
    """
    tujuan = mata_uang_tujuan.strip().upper()

    if not tujuan:
        raise ValueError(
            "Kode mata uang tidak boleh kosong."
        )

    try:
        response = requests.get(
            f"{BASE_URL}/latest",
            params={
                "from": "IDR",
                "to": tujuan,
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as error:
        raise ConnectionError(
            "Permintaan kurs terlalu lama. "
            "Silakan coba kembali."
        ) from error

    except requests.exceptions.HTTPError as error:
        status_code = (
            error.response.status_code
            if error.response is not None
            else "tidak diketahui"
        )

        raise ValueError(
            f"Gagal mengambil kurs. "
            f"Kode status HTTP: {status_code}."
        ) from error

    except requests.exceptions.ConnectionError as error:
        raise ConnectionError(
            "Tidak dapat terhubung ke layanan kurs. "
            "Periksa koneksi internet."
        ) from error

    except requests.exceptions.RequestException as error:
        raise ConnectionError(
            "Terjadi gangguan saat menghubungi "
            "layanan kurs."
        ) from error

    try:
        data = response.json()
    except ValueError as error:
        raise ValueError(
            "Respons dari layanan kurs bukan JSON yang valid."
        ) from error

    rates = data.get("rates")

    if not isinstance(rates, dict):
        raise ValueError(
            "Format data kurs dari server tidak sesuai."
        )

    if tujuan not in rates:
        raise ValueError(
            f"Mata uang '{tujuan}' tidak tersedia."
        )

    try:
        return float(rates[tujuan])
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Nilai kurs dari server tidak valid."
        ) from error


def harga_dalam_mata_uang(
    harga_idr: float,
    mata_uang_tujuan: str,
) -> str:
    """
    Mengonversi harga rupiah ke mata uang tujuan.

    Contoh hasil:
        USD 0.92
    """
    if harga_idr < 0:
        raise ValueError(
            "Harga IDR tidak boleh negatif."
        )

    tujuan = mata_uang_tujuan.strip().upper()

    if not tujuan:
        raise ValueError(
            "Kode mata uang tidak boleh kosong."
        )

    kurs = get_kurs(tujuan)
    hasil = harga_idr * kurs

    return f"{tujuan} {hasil:,.2f}"