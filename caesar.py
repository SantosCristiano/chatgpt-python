from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from functools import partial

class CaesarCipherApp(App):
    def build(self):
        self.shift = 3  # Default shift value
        self.output_label = Label(text="Output will be displayed here")

        text_input = TextInput(text="Enter text to encrypt/decrypt")
        shift_input = TextInput(text="3")
        encrypt_button = Button(text="Encrypt")
        decrypt_button = Button(text="Decrypt")

        encrypt_button.bind(on_press=partial(self.on_encrypt_decrypt, action='encrypt', text_input=text_input, shift_input=shift_input))
        decrypt_button.bind(on_press=partial(self.on_encrypt_decrypt, action='decrypt', text_input=text_input, shift_input=shift_input))

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Caesar Cipher Encryption/Decryption"))
        layout.add_widget(text_input)
        layout.add_widget(Label(text="Shift value:"))
        layout.add_widget(shift_input)
        layout.add_widget(encrypt_button)
        layout.add_widget(decrypt_button)
        layout.add_widget(self.output_label)

        return layout

    def on_encrypt_decrypt(self, instance, action, text_input, shift_input):
        text = text_input.text
        shift = int(shift_input.text)

        if action == 'encrypt':
            result = self.caesar_encrypt(text, shift)
        elif action == 'decrypt':
            result = self.caesar_decrypt(text, shift)

        self.output_label.text = result

    def caesar_encrypt(self, text, shift):
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                if char.islower():
                    encrypted_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                else:
                    encrypted_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted_text += char
        return encrypted_text

    def caesar_decrypt(self, text, shift):
        decrypted_text = ""
        for char in text:
            if char.isalpha():
                if char.islower():
                    decrypted_text += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                else:
                    decrypted_text += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted_text += char
        return decrypted_text

if __name__ == "__main__":
    CaesarCipherApp().run()
