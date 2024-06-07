import compress
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label

class FileCompressionApp(App):
    def compress_file(self, filename):
        with open(filename, 'rb') as f_in:
            with gzip.open(filename + '.gz', 'wb') as f_out:
                f_out.writelines(f_in)

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.file_chooser = FileChooserListView()
        self.layout.add_widget(self.file_chooser)
        compress_button = Button(text='Compress File')
        compress_button.bind(on_press=self.compress_selected_file)
        self.layout.add_widget(compress_button)
        return self.layout

    def compress_selected_file(self, instance):
        selected_file = self.file_chooser.selection
        if selected_file:
            self.compress_file(selected_file[0])
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text="File compressed successfully!"))
            save_button = Button(text='Save Compressed File', on_press=self.save_compressed_file)
            self.layout.add_widget(save_button)

    def save_compressed_file(self, instance):
        selected_file = self.file_chooser.selection
        if selected_file:
            filename = selected_file[0] + '.gz'
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text=f"Compressed file saved as: {filename}"))

if __name__ == '__main__':
    FileCompressionApp().run()
