import os
import win32com.client

def list_outlook_folders():
    """Lista todas las carpetas disponibles en Outlook para ayudar a identificar la estructura"""
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        
        print("Cuentas y carpetas disponibles:")
        print("-" * 50)
        
        # Listar todas las cuentas/carpetas principales
        for i in range(1, namespace.Folders.Count + 1):
            try:
                account = namespace.Folders.Item(i)
                print(f"Cuenta {i}: {account.Name}")
                
                # Listar subcarpetas
                for j in range(1, account.Folders.Count + 1):
                    try:
                        subfolder = account.Folders.Item(j)
                        print(f"  - {subfolder.Name}")
                    except:
                        continue
                print()
            except:
                continue
                
    except Exception as e:
        print(f"Error al listar carpetas: {e}")

def find_folder_by_name(folder_name):
    """Busca una carpeta por nombre en todas las cuentas disponibles"""
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        
        # Buscar en todas las cuentas
        for i in range(1, namespace.Folders.Count + 1):
            try:
                account = namespace.Folders.Item(i)
                
                # Buscar en las subcarpetas
                for j in range(1, account.Folders.Count + 1):
                    try:
                        subfolder = account.Folders.Item(j)
                        if subfolder.Name == folder_name:
                            print(f"Carpeta '{folder_name}' encontrada en cuenta: {account.Name}")
                            return subfolder
                    except:
                        continue
            except:
                continue
        
        print(f"No se encontró la carpeta '{folder_name}'")
        return None
        
    except Exception as e:
        print(f"Error al buscar carpeta: {e}")
        return None

def save_attachments_from_folder(folder_name, save_path):
    try:
        # Buscar la carpeta por nombre
        folder = find_folder_by_name(folder_name)
        
        if folder is None:
            print(f"\nNo se pudo encontrar la carpeta '{folder_name}'")
            print("Listando carpetas disponibles:")
            list_outlook_folders()
            return

        # Ensure the save directory exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        print(f"Procesando carpeta: {folder.Name}")
        print(f"Guardando archivos en: {save_path}")
        
        attachments_found = 0
        
        # Loop through items in the folder
        for item in folder.Items:
            if item.Class == 43:  # Check if the item is a mail item
                for attachment in item.Attachments:
                    if attachment.FileName.endswith(".xlsx"):
                        attachment_path = os.path.join(save_path, attachment.FileName)
                        attachment.SaveAsFile(attachment_path)
                        print(f"Saved {attachment.FileName} to {attachment_path}")
                        attachments_found += 1
        
        if attachments_found == 0:
            print("No se encontraron archivos .xlsx en la carpeta especificada")
        else:
            print(f"Se guardaron {attachments_found} archivos exitosamente")
            
    except Exception as e:
        print(f"Error en save_attachments_from_folder: {e}")
        print("\nListando carpetas disponibles para ayudarte:")
        list_outlook_folders()

if __name__ == "__main__":
    # Define the folder name and the path to save attachments
    folder_name = "Agente IA" # Cambia esto al nombre de tu carpeta
    current_path = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(current_path, "facturas")

    save_attachments_from_folder(folder_name, save_path)
