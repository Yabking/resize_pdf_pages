# PDF Resizing Web App

#### Video Demo: <https://www.youtube.com/watch?v=ZwSCH658Xl0> 

#### Description:
> **Disclaimer:**
> 
> Only install "Pymupdf" but not "Fitz" since there is an older version that could make it not work.
> 
> This README was written with the help of AI (ChatGPT) based on my own answers and explanations through a Q&A process.
> The ideas, project concept, and all core code implementation were done by me. AI was used for structuring and polishing the writing for clarity and readability.
This is a **PDF resizing web application** built with Flask. It allows users to upload PDF files—either by dropping them into a dropzone or selecting them manually—and automatically resizes every page to a consistent dimension. The goal is to make reading smoother by removing inconsistent page sizes, which can be especially annoying when reading manhwas or comics.

After uploading, the app checks if the file is valid and properly formatted. It looks out for renamed or corrupted files and handles errors gracefully. Once verified, it creates new pages with a standard width and height, then adjusts the content to fit perfectly inside. The resizing happens in batches of 10 pages to avoid overloading memory. Each batch is stored temporarily, and once all are processed, they’re stitched together in memory and downloaded automatically.

If something goes wrong—invalid file type, corrupted page, or server error—the user is shown a clear flash message.

---

### Why I Built It

I got tired of reading manhwas where every few pages were zoomed differently. I’d constantly have to adjust the zoom level, which broke the flow. So I decided to make a tool that automatically resizes pages to the same dimensions, giving a more consistent experience.

---

### Technologies Used

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript
* **Styling:** Bootstrap, TailwindCSS
* **Libraries:** PyMuPDF (fitz) for reading and editing PDFs
* **Other modules:** tempfile, io, os, werkzeug.utils

I considered using **Poppler** and **Pillow**, but both would have converted PDF pages into images, making text unsearchable. PyMuPDF offered a better and cleaner way to keep the text searchable while resizing efficiently.

---

### How It Works

1. User uploads or drops a PDF file.
2. The server validates the input and checks if it’s an actual PDF.
3. Pages are resized to a uniform dimension while keeping proportions intact.
4. Every 10 pages are processed and temporarily saved in batches.
5. After all batches finish, the app merges them into a single output file.
6. A JavaScript progress bar polls `/progress` to show live updates.
7. When done, the final PDF is sent for automatic download and a success message appears.

If anything fails, the app stops processing, flashes an error message, and prevents bad files from continuing.

---

### Design Decisions

The main design decision was to process PDFs in **batches** to prevent memory crashes. Instead of loading an entire large file into RAM, the app processes a few pages at a time and compiles them later. This divide-and-conquer method kept things efficient and stable.

The progress bar was another interesting problem. I implemented a polling system that requests the current progress from the server every 100ms and updates the progress bar width and percentage dynamically.

---

### Features

* Upload validation for real PDF files
* Batch-based processing for memory efficiency
* Real-time progress tracking
* Clear error and success feedback
* Automatic download after completion

---

### Challenges

The hardest part was managing **RAM usage** while processing large PDFs. At first, the app crashed when trying to load big files all at once. I solved it by dividing the work into small chunks, processing 10 pages at a time, then merging everything at the end.

Another tricky part was syncing the frontend and backend during progress updates. I had to find a balance between update speed and server load so it felt smooth without lagging or freezing.

---

### Future Improvements

If I had more time, I’d:

* Add a dedicated results page where users can manually redownload their resized file.
* Improve download reliability (so it can retry if it fails).
* Add support for other file types like images or Word documents.
* Allow custom dimensions for resizing.

---

### Use of AI

I used AI responsibly during development for **learning and optimization**, not code replacement.

* **Frontend layout:** AI helped me design the HTML/CSS layout since I wanted something clean and minimal.
* **Big file handling:** AI helped me set a 150mb limit on the files that can be uploaded(i was too lazy).
* **Debugging:** GitHub Copilot helped me fix my favicon setup.
* **Backend optimization:** ChatGPT helped review my Python logic for file handling and batch processing.
* **Docs clarification:** I used AI to better understand PyMuPDF’s methods and confirm how to use them safely.

All **core logic** (file processing, batching, progress tracking, error handling) was written by me. AI’s role was mainly advisory.

---

### Lessons Learned

I learned a lot about:

* File handling and temporary storage
* Managing memory while processing files
* Integrating external libraries like PyMuPDF
* Building user-friendly progress feedback systems
* Combining backend logic with a clean, interactive frontend

The project also made me appreciate how much better an app feels when it gives users real-time updates instead of just freezing while processing.

---

### Reflection

If I were to continue this project, I’d make downloading more robust, allow other file formats, and maybe even deploy it online for others to use.

It started out as a personal fix for a small annoyance, but turned into something I’m genuinely proud of. It’s efficient, simple, and solves a real problem I actually had.

---

**Project by:** yab
**Course:** CS50’s Introduction to Computer Science
**Year:** 2025
**Word count:** ~750