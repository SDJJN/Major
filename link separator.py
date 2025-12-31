from fpdf import FPDF

# Data: Episode number and Google Drive URLs
data = [
    ("Episode", "Google Drive URL"),
    (1, "https://drive.google.com/file/d/1kpzxnq5nQ_S3RrQISqDJ7EeBlqjY3nOL/view?usp=share_link"),
    (2, "https://drive.google.com/file/d/1w_zFu3Od4bXRgpfUF0f56W78qmAKXFHP/view?usp=share_link"),
    (3, "https://drive.google.com/file/d/1fhrKZzrp3y3ZxRYzXV5FfeMtmaqL7G57/view?usp=share_link"),
    (4, "https://drive.google.com/file/d/1piu3kIi-WRgrAZVbH7WJwvB0qO3GLUgV/view?usp=share_link"),
    (5, "https://drive.google.com/file/d/1xlozF0WxcbyT5i3dTePT7z6XQgGUg1ye/view?usp=share_link"),
    (6, "https://drive.google.com/file/d/1uIzYVxXPIIOJRw1sMpRO0dkYjUmJhpwi/view?usp=share_link"),
    (7, "https://drive.google.com/file/d/1MpaAmNdZnUplWBnWSiMiqZmL_B2R9wVN/view?usp=share_link"),
    (8, "https://drive.google.com/file/d/17k-zdabYIbFx88EQsgvLI3xejyf8JC6K/view?usp=share_link"),
    (9, "https://drive.google.com/file/d/1VfW0uOyXjKB29VXqo5_yRVZKjlSs0j2e/view?usp=share_link"),
    (10, "https://drive.google.com/file/d/1y6vaqRBKEAkqTWT1pl-xHpI3EwqXPyoT/view?usp=share_link"),
    (11, "https://drive.google.com/file/d/1HIGNRwCdKYJzYBdRtF8uZ1pPJceJxcbr/view?usp=share_link"),
    (12, "https://drive.google.com/file/d/192p9ZaSDgV0_-yWWyNaYWg0Dyl5H5A_9/view?usp=share_link"),
    (13, "https://drive.google.com/file/d/1sqUyH-_CQ2Q1wH9_gR2SKNVv5eIidGju/view?usp=share_link"),
    (14, "https://drive.google.com/file/d/1TJHARcxk_pCMqPo_Z6B4Vwsrm20duaW8/view?usp=share_link"),
    (15, "https://drive.google.com/file/d/1liEItZZsKX4_dIEZKi9_vGQhoc5P2RDx/view?usp=share_link"),
    (16, "https://drive.google.com/file/d/1cMIn1AmEGt5tVJauPSf13oAbfEBrnC02/view?usp=share_link"),
    (17, "https://drive.google.com/file/d/1WIDbvm73uf950yj2PTsJVC-bT9O56NEU/view?usp=share_link"),
    (18, "https://drive.google.com/file/d/1oWL0IufMTiDYRvQTdahRdhD8jn9QMdr4/view?usp=share_link"),
    (19, "https://drive.google.com/file/d/1s-_KTJRfkHQKWKLPhYC_2W85pt7AKWf2/view?usp=share_link"),
    (20, "https://drive.google.com/file/d/1xXZLUEnZw86_cRBrxdCZBwZtuRZ-jgeX/view?usp=sharing"),
    (21, "https://drive.google.com/file/d/1WCeyI_2m1Hx7UebV73eO_jxu6ODGNJSe/view?usp=share_link"),
    (22, "https://drive.google.com/file/d/1NfsFTul8k5TIA25yVJKtHJZTNKmjriYR/view?usp=share_link"),
    (23, "https://drive.google.com/file/d/1kuFpPx_YQTx8lHYBbxYseIy-rdepJGET/view?usp=share_link"),
    (24, "https://drive.google.com/file/d/16-JtiozK6ig30yzgBYCEgd4BtXNy7rvG/view?usp=share_link"),
    (25, "https://drive.google.com/file/d/1Qouq9aaeyop8-g5WNZWxrdk7IvS-2xpr/view?usp=share_link"),
    (26, "https://drive.google.com/file/d/1SaPsWR63RhRLjPxcyJvHbMWMDX-UNQTi/view?usp=share_link"),
    (27, "https://drive.google.com/file/d/1zvDn53_FJ5MKKsc3x0THhC-n7mKxuySi/view?usp=share_link"),
    (28, "https://drive.google.com/file/d/1L6QLNhd3Xd279Gnt2XUU3rXXmGdGBgOb/view?usp=share_link"),
    (29, "https://drive.google.com/file/d/1C9HXjJoPi0bagnGwEOZZ1lCJi801QQv4/view?usp=share_link"),
    (30, "https://drive.google.com/file/d/129U0Jq5lfInxcEEX69ONXOMf9jMPNVxD/view?usp=share_link"),
    (31, "https://drive.google.com/file/d/1Vp7zlsFcbs-ChLKplHP5kqjdVgYnC8-D/view?usp=share_link"),
    (32, "https://drive.google.com/file/d/1sJsBscKPW4SfxdMWBNzbTyyB-DIMWHIe/view?usp=share_link"),
    (33, "https://drive.google.com/file/d/1Wa2IgU2claRAQ2nOPujT0oDzZxO2ZY5w/view?usp=share_link"),
    (34, "https://drive.google.com/file/d/1HL6zZwuMSs2zduGhsZS5QD6G4_3gWI3h/view?usp=share_link"),
    (35, "https://drive.google.com/file/d/1mR6ykqgl_i9CaXoEqb7Z4Sy2jYQDDRr5/view?usp=share_link"),
    (36, "https://drive.google.com/file/d/1Zc6yrAZLQFTrmbOIBikVD84y8Jj2WtHS/view?usp=share_link"),
]

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Google Drive Links by Episode', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Column widths
w1 = 25
w2 = 155

# Header row
pdf.set_font('Arial', 'B', 12)
pdf.cell(w1, 10, data[0][0], border=1)
pdf.cell(w2, 10, data[0][1], border=1)
pdf.ln()

pdf.set_font('Arial', '', 11)

# Data rows with clickable URLs
for episode, url in data[1:]:
    pdf.cell(w1, 8, str(episode), border=1)
    
    # Save current position to set link later
    x = pdf.get_x()
    y = pdf.get_y()
    
    # Print the URL text
    pdf.set_text_color(0, 0, 255)  # Blue color for link
    pdf.cell(w2, 8, url, border=1, ln=0)
    pdf.set_text_color(0, 0, 0)  # Reset to black
    
    # Create a link annotation
    pdf.link(x, y, w2, 8, url)
    pdf.ln()

pdf.output("google_drive_links_episodes_clickable.pdf")
print("Clickable PDF created successfully!")
