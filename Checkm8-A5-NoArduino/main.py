import dfu_util

def main():
    try:
        # Example usage
        dfu_util.enter_dfu_mode()
        dfu_util.send_payload('payload_8940.bin')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()
