from utils.db import db
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for, json, send_file
from models.reportes import Reportes

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/reportes', methods=['GET', 'POST'])
def inicio():
   return render_template('reportes.html')