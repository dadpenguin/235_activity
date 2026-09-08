"""App entry point."""
from music import create_app
from music.adapters.memory_repository import MemoryRepository, populate
from flask import Flask, render_template, redirect, url_for, request
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User

app = create_app()
repo = MemoryRepository()
populate("music/adapters/data", repo)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False, Debug = True)