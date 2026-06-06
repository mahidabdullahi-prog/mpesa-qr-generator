import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def generate_mpesa_qr(paybill_number, account_number, amount, output_filename=None):
    """
    Generate a QR code for M-Pesa Paybill with account number and amount.
    
    Args:
        paybill_number (str): The Paybill number (e.g., "7121365")
        account_number (str): Customer's account number
        amount (str): Payment amount
        output_filename (str): Output file name (optional)
    
    Returns:
        str: Path to the saved QR code image
    """
    
    # Create the QR code data string
    # Format: paybill_number|account_number|amount
    qr_data = f"{paybill_number}|{account_number}|{amount}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create the image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Generate output filename if not provided
    if output_filename is None:
        output_filename = f"mpesa_paybill_{paybill_number}_{account_number}.png"
    
    # Save the image
    img.save(output_filename)
    print(f"✓ QR code generated successfully: {output_filename}")
    print(f"  Paybill: {paybill_number}")
    print(f"  Account: {account_number}")
    print(f"  Amount: {amount}")
    
    return output_filename


def generate_qr_with_details(paybill_number, account_number, amount, output_filename=None):
    """
    Generate a QR code with payment details displayed below it.
    
    Args:
        paybill_number (str): The Paybill number
        account_number (str): Customer's account number
        amount (str): Payment amount
        output_filename (str): Output file name (optional)
    
    Returns:
        str: Path to the saved image with QR code and details
    """
    
    # Create the QR code data
    qr_data = f"{paybill_number}|{account_number}|{amount}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Create a new image with space for text
    width = qr_img.width
    height = qr_img.height + 150
    
    img = Image.new('RGB', (width, height), color='white')
    
    # Paste QR code
    img.paste(qr_img, (0, 0))
    
    # Add text details
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to default if not available
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Add payment details text
    text_y = qr_img.height + 10
    draw.text((10, text_y), "M-Pesa Paybill Payment", fill='black', font=font_large)
    draw.text((10, text_y + 30), f"Paybill: {paybill_number}", fill='black', font=font_small)
    draw.text((10, text_y + 50), f"Account: {account_number}", fill='black', font=font_small)
    draw.text((10, text_y + 70), f"Amount: KES {amount}", fill='black', font=font_small)
    
    # Generate output filename if not provided
    if output_filename is None:
        output_filename = f"mpesa_paybill_{paybill_number}_{account_number}_with_details.png"
    
    # Save the image
    img.save(output_filename)
    print(f"✓ QR code with details generated: {output_filename}")
    
    return output_filename


def main():
    """Main function for interactive QR code generation"""
    print("=" * 50)
    print("M-Pesa Paybill QR Code Generator")
    print("=" * 50)
    
    # Fixed Paybill number
    paybill_number = "7121365"
    
    # Get user input
    account_number = input("\nEnter Account Number: ").strip()
    amount = input("Enter Amount (e.g., 1000): ").strip()
    
    if not account_number or not amount:
        print("✗ Error: Account number and amount are required!")
        return
    
    try:
        # Validate amount is a number
        float(amount)
    except ValueError:
        print("✗ Error: Amount must be a valid number!")
        return
    
    # Ask user preference
    print("\nSelect QR code type:")
    print("1. QR code only")
    print("2. QR code with payment details")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        generate_mpesa_qr(paybill_number, account_number, amount)
    elif choice == "2":
        generate_qr_with_details(paybill_number, account_number, amount)
    else:
        print("✗ Invalid choice!")


if __name__ == "__main__":
    main()
