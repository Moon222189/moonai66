{
  "functions": {
    "api/learn.py": {
      "runtime": "python3.11"
    }
  },
  "builds": [
    {
      "src": "api/*.py",
      "use": "@vercel/python"
    }
  ]
}
