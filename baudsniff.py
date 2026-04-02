import serial
import time
import sys

BAUDRATES = [110, 300, 600, 1200, 2400, 4800, 9600,
             14400, 19200, 38400, 57600, 115200, 128000, 256000]

MIN_PRINTABLE  = 10
MIN_RATIO      = 50.0
POLL_INTERVAL  = 0.3

def count_printable(data: bytes) -> int:
    return sum(1 for b in data if 0x20 <= b <= 0x7E or b in (0x0A, 0x0D))

def wait_for_signal(port):
    print("[*] Waiting for signal on the device...")
    print("[*] Power on the device now.\n")
    while True:
        for baud in BAUDRATES:
            try:
                ser = serial.Serial(port, baud, timeout=0.3)
                ser.write(b"\r\n")
                time.sleep(0.2)
                data = ser.read(64)
                ser.close()
                if len(data) > 0:
                    print("[+] Signal detected!\n")
                    time.sleep(3)
                    return
            except Exception:
                pass
        time.sleep(POLL_INTERVAL)

def test_baud(port, baud):
    try:
        ser = serial.Serial(port, baud, timeout=1)
        time.sleep(0.3)
        ser.write(b"\r\n")
        time.sleep(0.5)
        data = ser.read(256)
        ser.close()
        score = count_printable(data)
        ratio = score / max(len(data), 1) * 100
        return score, ratio
    except Exception:
        return 0, 0.0

def main():
    if len(sys.argv) < 2:
        print("Usage: python detect.py <PORT>")
        print("Example: python detect.py COM8")
        sys.exit(1)

    port = sys.argv[1]

    wait_for_signal(port)

    print(f"[*] Baud rate bruteforce on {port}\n")
    results = []

    for baud in BAUDRATES:
        score, ratio = test_baud(port, baud)
        candidate = "<<< CANDIDATE" if score >= MIN_PRINTABLE and ratio >= MIN_RATIO else ""
        print(f"  {baud:>7} baud | {score:>4} ASCII chars | {ratio:>5.1f}% readable | {candidate}")
        results.append((ratio, score, baud))

    results.sort(reverse=True)
    best_ratio, best_score, best_baud = results[0]

    print(f"\n[+] Best match: {best_baud} baud  ({best_score} chars, {best_ratio:.1f}% readable)")
    print(f"[+] Use this baud rate in PuTTY or the dump script.")

if __name__ == "__main__":
    main()
