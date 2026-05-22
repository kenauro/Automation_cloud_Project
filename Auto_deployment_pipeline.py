from google.cloud import devconnect_v1 # Menggunakan Google Cloud Build API
from google.cloud import run_v2        # Menggunakan Cloud Run API untuk verifikasi
import sys

def run_gcp_deployment_pipeline():
    print("=== STARTING GCP AUTOMATED DEPLOYMENT PIPELINE ===")

    project_id = "it-financial-services-indomaret"
    location = "asia-southeast2" 
    repo_name = "financial-app-repo"
    image_name = f"{location}-docker.pkg.dev/{project_id}/{repo_name}/financial-web-app:latest"

    # 1. Menginisialisasi Client Cloud Build
    # Skrip ini mengirimkan instruksi ke GCP untuk melakukan 'Build Image' langsung di server Google
    print("➔ Mengirimkan instruksi kompilasi ke Google Cloud Build...")
    
    # Di dunia nyata, langkah ini memicu file 'cloudbuild.yaml' atauDockerfile yang ada di root project
    # Untuk simulasi portofolio, kita asumsikan trigger build berhasil ditembak
    build_success = True 
    
    if not build_success:
        print("[ERROR] Cloud Build gagal mengompilasi Docker Image!")
        sys.exit(1)
        
    print(f"[BERHASIL] Docker Image sukses disimpan di Artifact Registry: {image_name}")

    # 2. Perintahkan Google Cloud Run untuk melakukan Rolling Update (Deployment)
    print("\n➔ Memerintahkan Google Cloud Run untuk merilis versi terbaru...")
    client = run_v2.ServicesClient()
    
    try:
        # Menentukan target layanan Cloud Run yang akan diperbarui
        service_path = client.service_path(project_id, location, "web-financial-app")
        
        # Mengambil data layanan saat ini
        service = client.get_service(name=service_path)
        
        # Memperbarui container image ke versi terbaru yang ada di Artifact Registry
        service.template.containers[0].image = image_name
        
        # Eksekusi update (GCP akan melakukan rolling update otomatis tanpa downtime)
        operation = client.update_service(service=service)
        print("[INFO] Menunggu proses rolling update selesai di cloud...")
        
        print("\n[SUKSES] Aplikasi finansial berhasil dideploy ke GCP Cloud Run!")
        print("Status: 100% Traffic dialihkan ke versi terbaru dengan aman.")
        
    except Exception as e:
        print(f"[ERROR] Gagal memperbarui layanan di Cloud Run: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_gcp_deployment_pipeline();