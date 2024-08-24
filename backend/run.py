import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:get_app",
        host="0.0.0.0",
        port=8081,
        log_level="debug",
        reload=True,
        factory=True,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
