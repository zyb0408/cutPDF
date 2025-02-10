import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QLineEdit, QTabWidget, QHBoxLayout

class PDFtoImageConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("选择PDF文件并指定输出文件夹", self)
        layout.addWidget(self.label)
        
        self.btn_open_pdf = QPushButton('选择PDF文件', self)
        self.btn_open_pdf.clicked.connect(self.open_pdf)
        layout.addWidget(self.btn_open_pdf)
        
        self.btn_open_folder = QPushButton('选择输出文件夹', self)
        self.btn_open_folder.clicked.connect(self.open_folder)
        layout.addWidget(self.btn_open_folder)
        
        self.dpi_label = QLabel("设置DPI（默认400）:", self)
        layout.addWidget(self.dpi_label)
        
        self.dpi_input = QLineEdit(self)
        self.dpi_input.setText("400")
        layout.addWidget(self.dpi_input)
        
        self.btn_convert = QPushButton('转换', self)
        self.btn_convert.clicked.connect(self.convert_pdf_to_images)
        layout.addWidget(self.btn_convert)
        
        self.setLayout(layout)
        
        self.pdf_path = ""
        self.output_folder = ""
    
    def open_pdf(self):
        options = QFileDialog.Options()
        self.pdf_path, _ = QFileDialog.getOpenFileName(self, "选择PDF文件", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if self.pdf_path:
            self.label.setText(f"PDF文件: {self.pdf_path}")
    
    def open_folder(self):
        options = QFileDialog.Options()
        self.output_folder = QFileDialog.getExistingDirectory(self, "选择输出文件夹", options=options)
        if self.output_folder:
            self.label.setText(f"输出文件夹: {self.output_folder}")
    
    def convert_pdf_to_images(self):
        if not self.pdf_path or not self.output_folder:
            self.label.setText("请先选择PDF文件和输出文件夹")
            return
        
        try:
            dpi = int(self.dpi_input.text())
        except ValueError:
            QMessageBox.warning(self, "输入错误", "请确保DPI是一个有效的整数")
            return
        
        pdf_document = fitz.open(self.pdf_path)
        num_pages = len(pdf_document)
        
        for page_num in range(num_pages):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap(dpi=dpi)
            output_path = f"{self.output_folder}/page_{page_num + 1}.jpeg"
            pix.save(output_path)
        
        self.label.setText("转换完成")
        QMessageBox.information(self, "完成", f"PDF文件已成功转换为JPEG图片，保存在 {self.output_folder}")

class ImagestoPDFConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("选择图片文件并指定输出PDF文件", self)
        layout.addWidget(self.label)
        
        self.btn_open_images = QPushButton('选择图片文件', self)
        self.btn_open_images.clicked.connect(self.open_images)
        layout.addWidget(self.btn_open_images)
        
        self.btn_open_pdf = QPushButton('选择输出PDF文件位置', self)
        self.btn_open_pdf.clicked.connect(self.open_pdf_file)
        layout.addWidget(self.btn_open_pdf)
        
        self.btn_convert = QPushButton('合并', self)
        self.btn_convert.clicked.connect(self.merge_images_to_pdf)
        layout.addWidget(self.btn_convert)
        
        self.setLayout(layout)
        
        self.image_files = []
        self.output_pdf_path = ""
    
    def open_images(self):
        options = QFileDialog.Options()
        self.image_files, _ = QFileDialog.getOpenFileNames(self, "选择图片文件", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif);;All Files (*)", options=options)
        if self.image_files:
            self.label.setText(f"选择的图片文件 ({len(self.image_files)} 个)")
    
    def open_pdf_file(self):
        options = QFileDialog.Options()
        self.output_pdf_path, _ = QFileDialog.getSaveFileName(self, "保存PDF文件", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if self.output_pdf_path:
            self.label.setText(f"输出PDF文件: {self.output_pdf_path}")
    
    def merge_images_to_pdf(self):
        if not self.image_files or not self.output_pdf_path:
            self.label.setText("请先选择图片文件和输出PDF文件位置")
            return
        
        from PIL import Image
        
        images = []
        for image_file in self.image_files:
            image = Image.open(image_file).convert("RGB")
            images.append(image)
        
        images[0].save(self.output_pdf_path, save_all=True, append_images=images[1:])
        
        self.label.setText("合并完成")
        QMessageBox.information(self, "完成", f"图片已成功合并为PDF文件，保存在 {self.output_pdf_path}")

class PDFtoMultiplePDFConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("选择PDF文件并指定输出文件夹", self)
        layout.addWidget(self.label)
        
        self.btn_open_pdf = QPushButton('选择PDF文件', self)
        self.btn_open_pdf.clicked.connect(self.open_pdf)
        layout.addWidget(self.btn_open_pdf)
        
        self.btn_open_folder = QPushButton('选择输出文件夹', self)
        self.btn_open_folder.clicked.connect(self.open_folder)
        layout.addWidget(self.btn_open_folder)
        
        self.btn_convert = QPushButton('分割', self)
        self.btn_convert.clicked.connect(self.split_pdf)
        layout.addWidget(self.btn_convert)
        
        self.setLayout(layout)
        
        self.pdf_path = ""
        self.output_folder = ""
    
    def open_pdf(self):
        options = QFileDialog.Options()
        self.pdf_path, _ = QFileDialog.getOpenFileName(self, "选择PDF文件", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if self.pdf_path:
            self.label.setText(f"PDF文件: {self.pdf_path}")
    
    def open_folder(self):
        options = QFileDialog.Options()
        self.output_folder = QFileDialog.getExistingDirectory(self, "选择输出文件夹", options=options)
        if self.output_folder:
            self.label.setText(f"输出文件夹: {self.output_folder}")
    
    def split_pdf(self):
        if not self.pdf_path or not self.output_folder:
            self.label.setText("请先选择PDF文件和输出文件夹")
            return
        
        pdf_document = fitz.open(self.pdf_path)
        num_pages = len(pdf_document)
        
        for page_num in range(num_pages):
            output_pdf_path = f"{self.output_folder}/page_{page_num + 1}.pdf"
            writer = fitz.open()
            writer.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
            writer.save(output_pdf_path)
            writer.close()
        
        self.label.setText("分割完成")
        QMessageBox.information(self, "完成", f"PDF文件已成功分割为多个PDF文件，保存在 {self.output_folder}")

class MultiplePDFtoSinglePDFConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("选择PDF文件并指定输出PDF文件", self)
        layout.addWidget(self.label)
        
        self.btn_open_pdfs = QPushButton('选择PDF文件', self)
        self.btn_open_pdfs.clicked.connect(self.open_pdfs)
        layout.addWidget(self.btn_open_pdfs)
        
        self.btn_open_pdf = QPushButton('选择输出PDF文件位置', self)
        self.btn_open_pdf.clicked.connect(self.open_pdf_file)
        layout.addWidget(self.btn_open_pdf)
        
        self.btn_convert = QPushButton('合并', self)
        self.btn_convert.clicked.connect(self.merge_pdfs)
        layout.addWidget(self.btn_convert)
        
        self.setLayout(layout)
        
        self.pdf_files = []
        self.output_pdf_path = ""
    
    def open_pdfs(self):
        options = QFileDialog.Options()
        self.pdf_files, _ = QFileDialog.getOpenFileNames(self, "选择PDF文件", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if self.pdf_files:
            self.label.setText(f"选择的PDF文件 ({len(self.pdf_files)} 个)")
    
    def open_pdf_file(self):
        options = QFileDialog.Options()
        self.output_pdf_path, _ = QFileDialog.getSaveFileName(self, "保存PDF文件", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if self.output_pdf_path:
            self.label.setText(f"输出PDF文件: {self.output_pdf_path}")
    
    def merge_pdfs(self):
        if not self.pdf_files or not self.output_pdf_path:
            self.label.setText("请先选择PDF文件和输出PDF文件位置")
            return
        
        writer = fitz.open()
        
        for pdf_file in self.pdf_files:
            reader = fitz.open(pdf_file)
            writer.insert_pdf(reader)
        
        writer.save(self.output_pdf_path)
        writer.close()
        
        self.label.setText("合并完成")
        QMessageBox.information(self, "完成", f"PDF文件已成功合并为一个PDF文件，保存在 {self.output_pdf_path}")

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('PDF 和 图片转换工具')
        self.setGeometry(100, 100, 400, 300)
        
        tabs = QTabWidget()
        self.tab1 = PDFtoImageConverter()
        self.tab2 = ImagestoPDFConverter()
        self.tab3 = PDFtoMultiplePDFConverter()
        self.tab4 = MultiplePDFtoSinglePDFConverter()
        
        tabs.addTab(self.tab1, 'PDF to Images')
        tabs.addTab(self.tab2, 'Images to PDF')
        tabs.addTab(self.tab3, 'PDF to Multiple PDFs')
        tabs.addTab(self.tab4, 'Multiple PDFs to Single PDF')
        
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())