# remember Yousef llm serve
this repository make auto response based on Ollama 3.1 and way of freedom document

این پروژه به یاد یوسف قبادی ساخته شده است.
ایده اصلی این هست که ما بتوانیم پاسخگویی و سرچ هوشمند روی مستندات دسترسی به اینترنت آزاد داشته باشیم.


این برنامه بر پایه اولا ساخته است و نیاز به داشتن GPU برای اجرا می باشد.

برای اجرا کردن برنامه دستورات زیر را پیروی کنید:

حتما باید داکر را روی سیسیتم نصب داشته باشید.

```
docker build -t llm-docs-ollama-app .
```

با دستور زیر تمامی داکر ها را اجرا کنید:
فایل .env را به صورت دستی ایجاد کنید

```
sudo docker-compose up
```

 حتما باید GPU روی سیستم شما نصب باشد با دستور زیر می توانید چک کنید

```
nvidia-smi -l 1
```

حالا شما باید مدل های اولاما رو دانلود کنید:

```
sudo docker-compose -f docker-compose.yml exec ollama /bin/sh 
ollama run nomic-embed-text
ollama run llama3.1
```

با ظاهر شدن پیغام زیر اولا روی پورت ۸۰۸۰ اجرا میشود

‍‍‍```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```