
import playwright
import moviepy.editor as mp

# Crear un navegador
async with playwright.start() as browser:
    context = await browser.new_context()
    page = await context.new_page()

    # Lista de URL
    urls = [
        "https://www.ejemplo1.com",
        "https://www.ejemplo2.com",
        "https://www.ejemplo3.com",
    ]

    # Crear un lienzo de video
    video = mp.VideoFileClip("background.mp4")

    # Recorrer las URL y agregar screenshots al video
    for url in urls:
        await page.goto(url)
        screenshot = await page.screenshot(full_page=True)
        image = mp.ImageClip(screenshot)
        video = video.set_duration(video.duration + image.duration)
        video = mp.CompositeVideoClip([video, image])

# Agregar música
audio = mp.AudioFileClip("musica.mp3")
video = video.set_audio(audio)

# Guardar el video final
video.write_videofile("video_final.mp4")

