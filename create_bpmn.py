#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to generate BPMN (Business Process Model and Notation) for HRM System in draw.io format
"""

import xml.etree.ElementTree as ET

def create_bpmn():
    """Create BPMN diagrams for HRM System"""
    
    root = ET.Element('mxGraphModel')
    root.set('dx', '1800')
    root.set('dy', '1400')
    root.set('gridSize', '10')
    root.set('guides', '1')
    root.set('tooltips', '1')
    root.set('connect', '1')
    root.set('arrows', '1')
    root.set('fold', '1')
    root.set('page', '1')
    root.set('pageScale', '1')
    root.set('pageWidth', '1800')
    root.set('pageHeight', '2400')
    root.set('background', '#ffffff')
    root.set('math', '0')
    root.set('shadow', '0')
    
    root_cell = ET.SubElement(root, 'root')
    
    default_cell1 = ET.SubElement(root_cell, 'mxCell')
    default_cell1.set('id', '0')
    default_cell1.set('parent', '')
    
    default_cell2 = ET.SubElement(root_cell, 'mxCell')
    default_cell2.set('id', '1')
    default_cell2.set('parent', '0')
    
    cell_id = 100
    
    # ===== PROCESS 1: EMPLOYEE ONBOARDING =====
    
    title1 = ET.SubElement(root_cell, 'mxCell')
    title1.set('id', str(cell_id))
    title1.set('value', 'PROCESS 1: Employee Onboarding')
    title1.set('style', 'text;fontSize=16;fontStyle=1;align=center;strokeColor=none;fillColor=none')
    title1.set('vertex', '1')
    title1.set('parent', '1')
    geo = ET.SubElement(title1, 'mxGeometry')
    geo.set('x', '50')
    geo.set('y', '20')
    geo.set('width', '600')
    geo.set('height', '30')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Start Event
    start1 = ET.SubElement(root_cell, 'mxCell')
    start1.set('id', str(cell_id))
    start1.set('value', 'Admin Initiates\nEmployee Creation')
    start1.set('style', 'ellipse;whiteSpace=wrap;html=1;fillColor=#90EE90;strokeColor=#228B22;strokeWidth=2')
    start1.set('vertex', '1')
    start1.set('parent', '1')
    geo = ET.SubElement(start1, 'mxGeometry')
    geo.set('x', '80')
    geo.set('y', '70')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    start1_id = cell_id
    cell_id += 1
    
    # Task 1: Fill Form
    task1_1 = ET.SubElement(root_cell, 'mxCell')
    task1_1.set('id', str(cell_id))
    task1_1.set('value', 'Fill Employee\nInformation Form')
    task1_1.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task1_1.set('vertex', '1')
    task1_1.set('parent', '1')
    geo = ET.SubElement(task1_1, 'mxGeometry')
    geo.set('x', '280')
    geo.set('y', '70')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task1_1_id = cell_id
    cell_id += 1
    
    # Task 2: Validate
    task1_2 = ET.SubElement(root_cell, 'mxCell')
    task1_2.set('id', str(cell_id))
    task1_2.set('value', 'System Validates\nData')
    task1_2.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task1_2.set('vertex', '1')
    task1_2.set('parent', '1')
    geo = ET.SubElement(task1_2, 'mxGeometry')
    geo.set('x', '480')
    geo.set('y', '70')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task1_2_id = cell_id
    cell_id += 1
    
    # Gateway: Valid?
    gateway1 = ET.SubElement(root_cell, 'mxCell')
    gateway1.set('id', str(cell_id))
    gateway1.set('value', 'Valid?')
    gateway1.set('style', 'rhombus;whiteSpace=wrap;html=1;fillColor=#FFD700;strokeColor=#FFA500;strokeWidth=2')
    gateway1.set('vertex', '1')
    gateway1.set('parent', '1')
    geo = ET.SubElement(gateway1, 'mxGeometry')
    geo.set('x', '495')
    geo.set('y', '200')
    geo.set('width', '90')
    geo.set('height', '90')
    geo.set('as', 'geometry')
    gateway1_id = cell_id
    cell_id += 1
    
    # Task: Show Error
    task1_err = ET.SubElement(root_cell, 'mxCell')
    task1_err.set('id', str(cell_id))
    task1_err.set('value', 'Show Error\nMessage')
    task1_err.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#FF6B6B;strokeColor=#DC143C;strokeWidth=2')
    task1_err.set('vertex', '1')
    task1_err.set('parent', '1')
    geo = ET.SubElement(task1_err, 'mxGeometry')
    geo.set('x', '700')
    geo.set('y', '210')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task1_err_id = cell_id
    cell_id += 1
    
    # Task: Create User Account
    task1_3 = ET.SubElement(root_cell, 'mxCell')
    task1_3.set('id', str(cell_id))
    task1_3.set('value', 'Create User\nAccount')
    task1_3.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task1_3.set('vertex', '1')
    task1_3.set('parent', '1')
    geo = ET.SubElement(task1_3, 'mxGeometry')
    geo.set('x', '280')
    geo.set('y', '210')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task1_3_id = cell_id
    cell_id += 1
    
    # Task: Save to DB
    task1_4 = ET.SubElement(root_cell, 'mxCell')
    task1_4.set('id', str(cell_id))
    task1_4.set('value', 'Save to\nDatabase')
    task1_4.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task1_4.set('vertex', '1')
    task1_4.set('parent', '1')
    geo = ET.SubElement(task1_4, 'mxGeometry')
    geo.set('x', '80')
    geo.set('y', '350')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task1_4_id = cell_id
    cell_id += 1
    
    # Task: Send Email
    task1_5 = ET.SubElement(root_cell, 'mxCell')
    task1_5.set('id', str(cell_id))
    task1_5.set('value', 'Send Welcome\nEmail')
    task1_5.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task1_5.set('vertex', '1')
    task1_5.set('parent', '1')
    geo = ET.SubElement(task1_5, 'mxGeometry')
    geo.set('x', '280')
    geo.set('y', '350')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task1_5_id = cell_id
    cell_id += 1
    
    # End Event: Success
    end1_ok = ET.SubElement(root_cell, 'mxCell')
    end1_ok.set('id', str(cell_id))
    end1_ok.set('value', 'Employee\nOnboarded')
    end1_ok.set('style', 'ellipse;whiteSpace=wrap;html=1;fillColor=#90EE90;strokeColor=#228B22;strokeWidth=2')
    end1_ok.set('vertex', '1')
    end1_ok.set('parent', '1')
    geo = ET.SubElement(end1_ok, 'mxGeometry')
    geo.set('x', '480')
    geo.set('y', '350')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    end1_ok_id = cell_id
    cell_id += 1
    
    # End Event: Error
    end1_err = ET.SubElement(root_cell, 'mxCell')
    end1_err.set('id', str(cell_id))
    end1_err.set('value', 'Error\nNotified')
    end1_err.set('style', 'ellipse;whiteSpace=wrap;html=1;fillColor=#FFB6C1;strokeColor=#DC143C;strokeWidth=2')
    end1_err.set('vertex', '1')
    end1_err.set('parent', '1')
    geo = ET.SubElement(end1_err, 'mxGeometry')
    geo.set('x', '700')
    geo.set('y', '350')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    end1_err_id = cell_id
    cell_id += 1
    
    # ===== PROCESS 2: LEAVE REQUEST WORKFLOW =====
    
    title2 = ET.SubElement(root_cell, 'mxCell')
    title2.set('id', str(cell_id))
    title2.set('value', 'PROCESS 2: Leave Request Workflow')
    title2.set('style', 'text;fontSize=16;fontStyle=1;align=center;strokeColor=none;fillColor=none')
    title2.set('vertex', '1')
    title2.set('parent', '1')
    geo = ET.SubElement(title2, 'mxGeometry')
    geo.set('x', '900')
    geo.set('y', '20')
    geo.set('width', '600')
    geo.set('height', '30')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Start: Employee Requests Leave
    start2 = ET.SubElement(root_cell, 'mxCell')
    start2.set('id', str(cell_id))
    start2.set('value', 'Employee\nRequests Leave')
    start2.set('style', 'ellipse;whiteSpace=wrap;html=1;fillColor=#90EE90;strokeColor=#228B22;strokeWidth=2')
    start2.set('vertex', '1')
    start2.set('parent', '1')
    geo = ET.SubElement(start2, 'mxGeometry')
    geo.set('x', '930')
    geo.set('y', '70')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    start2_id = cell_id
    cell_id += 1
    
    # Task: Submit Leave Form
    task2_1 = ET.SubElement(root_cell, 'mxCell')
    task2_1.set('id', str(cell_id))
    task2_1.set('value', 'Submit Leave\nRequest Form')
    task2_1.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task2_1.set('vertex', '1')
    task2_1.set('parent', '1')
    geo = ET.SubElement(task2_1, 'mxGeometry')
    geo.set('x', '1130')
    geo.set('y', '70')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task2_1_id = cell_id
    cell_id += 1
    
    # Task: Validate Dates
    task2_2 = ET.SubElement(root_cell, 'mxCell')
    task2_2.set('id', str(cell_id))
    task2_2.set('value', 'Validate\nDates')
    task2_2.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task2_2.set('vertex', '1')
    task2_2.set('parent', '1')
    geo = ET.SubElement(task2_2, 'mxGeometry')
    geo.set('x', '1330')
    geo.set('y', '70')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task2_2_id = cell_id
    cell_id += 1
    
    # Gateway: Dates Valid?
    gateway2 = ET.SubElement(root_cell, 'mxCell')
    gateway2.set('id', str(cell_id))
    gateway2.set('value', 'Valid?')
    gateway2.set('style', 'rhombus;whiteSpace=wrap;html=1;fillColor=#FFD700;strokeColor=#FFA500;strokeWidth=2')
    gateway2.set('vertex', '1')
    gateway2.set('parent', '1')
    geo = ET.SubElement(gateway2, 'mxGeometry')
    geo.set('x', '1345')
    geo.set('y', '200')
    geo.set('width', '90')
    geo.set('height', '90')
    geo.set('as', 'geometry')
    gateway2_id = cell_id
    cell_id += 1
    
    # Task: Notify Manager
    task2_3 = ET.SubElement(root_cell, 'mxCell')
    task2_3.set('id', str(cell_id))
    task2_3.set('value', 'Set Status to\nPENDING')
    task2_3.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task2_3.set('vertex', '1')
    task2_3.set('parent', '1')
    geo = ET.SubElement(task2_3, 'mxGeometry')
    geo.set('x', '1130')
    geo.set('y', '210')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task2_3_id = cell_id
    cell_id += 1
    
    # Task: Send Notification
    task2_4 = ET.SubElement(root_cell, 'mxCell')
    task2_4.set('id', str(cell_id))
    task2_4.set('value', 'Notify Manager\nfor Approval')
    task2_4.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task2_4.set('vertex', '1')
    task2_4.set('parent', '1')
    geo = ET.SubElement(task2_4, 'mxGeometry')
    geo.set('x', '930')
    geo.set('y', '210')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task2_4_id = cell_id
    cell_id += 1
    
    # Gateway: Approved?
    gateway2_b = ET.SubElement(root_cell, 'mxCell')
    gateway2_b.set('id', str(cell_id))
    gateway2_b.set('value', 'Approved?')
    gateway2_b.set('style', 'rhombus;whiteSpace=wrap;html=1;fillColor=#FFD700;strokeColor=#FFA500;strokeWidth=2')
    gateway2_b.set('vertex', '1')
    gateway2_b.set('parent', '1')
    geo = ET.SubElement(gateway2_b, 'mxGeometry')
    geo.set('x', '1030')
    geo.set('y', '340')
    geo.set('width', '90')
    geo.set('height', '90')
    geo.set('as', 'geometry')
    gateway2_b_id = cell_id
    cell_id += 1
    
    # Task: Approve
    task2_approve = ET.SubElement(root_cell, 'mxCell')
    task2_approve.set('id', str(cell_id))
    task2_approve.set('value', 'Update Status\nto APPROVED')
    task2_approve.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task2_approve.set('vertex', '1')
    task2_approve.set('parent', '1')
    geo = ET.SubElement(task2_approve, 'mxGeometry')
    geo.set('x', '930')
    geo.set('y', '480')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task2_approve_id = cell_id
    cell_id += 1
    
    # Task: Reject
    task2_reject = ET.SubElement(root_cell, 'mxCell')
    task2_reject.set('id', str(cell_id))
    task2_reject.set('value', 'Update Status\nto REJECTED')
    task2_reject.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#FF6B6B;strokeColor=#DC143C;strokeWidth=2')
    task2_reject.set('vertex', '1')
    task2_reject.set('parent', '1')
    geo = ET.SubElement(task2_reject, 'mxGeometry')
    geo.set('x', '1130')
    geo.set('y', '480')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task2_reject_id = cell_id
    cell_id += 1
    
    # Task: Send Employee Notification
    task2_notif = ET.SubElement(root_cell, 'mxCell')
    task2_notif.set('id', str(cell_id))
    task2_notif.set('value', 'Send Email\nNotification')
    task2_notif.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task2_notif.set('vertex', '1')
    task2_notif.set('parent', '1')
    geo = ET.SubElement(task2_notif, 'mxGeometry')
    geo.set('x', '1030')
    geo.set('y', '620')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task2_notif_id = cell_id
    cell_id += 1
    
    # End Event: Leave Processed
    end2 = ET.SubElement(root_cell, 'mxCell')
    end2.set('id', str(cell_id))
    end2.set('value', 'Leave\nProcessed')
    end2.set('style', 'ellipse;whiteSpace=wrap;html=1;fillColor=#90EE90;strokeColor=#228B22;strokeWidth=2')
    end2.set('vertex', '1')
    end2.set('parent', '1')
    geo = ET.SubElement(end2, 'mxGeometry')
    geo.set('x', '1030')
    geo.set('y', '760')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    end2_id = cell_id
    cell_id += 1
    
    # Error End
    end2_err = ET.SubElement(root_cell, 'mxCell')
    end2_err.set('id', str(cell_id))
    end2_err.set('value', 'Request\nRejected')
    end2_err.set('style', 'ellipse;whiteSpace=wrap;html=1;fillColor=#FFB6C1;strokeColor=#DC143C;strokeWidth=2')
    end2_err.set('vertex', '1')
    end2_err.set('parent', '1')
    geo = ET.SubElement(end2_err, 'mxGeometry')
    geo.set('x', '1330')
    geo.set('y', '340')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    end2_err_id = cell_id
    cell_id += 1
    
    # ===== PROCESS 3: ATTENDANCE RECORDING =====
    
    title3 = ET.SubElement(root_cell, 'mxCell')
    title3.set('id', str(cell_id))
    title3.set('value', 'PROCESS 3: Daily Attendance Recording')
    title3.set('style', 'text;fontSize=16;fontStyle=1;align=center;strokeColor=none;fillColor=none')
    title3.set('vertex', '1')
    title3.set('parent', '1')
    geo = ET.SubElement(title3, 'mxGeometry')
    geo.set('x', '50')
    geo.set('y', '520')
    geo.set('width', '600')
    geo.set('height', '30')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Start Event
    start3 = ET.SubElement(root_cell, 'mxCell')
    start3.set('id', str(cell_id))
    start3.set('value', 'Admin Accesses\nAttendance Page')
    start3.set('style', 'ellipse;whiteSpace=wrap;html=1;fillColor=#90EE90;strokeColor=#228B22;strokeWidth=2')
    start3.set('vertex', '1')
    start3.set('parent', '1')
    geo = ET.SubElement(start3, 'mxGeometry')
    geo.set('x', '80')
    geo.set('y', '570')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    start3_id = cell_id
    cell_id += 1
    
    # Task: Select Date
    task3_1 = ET.SubElement(root_cell, 'mxCell')
    task3_1.set('id', str(cell_id))
    task3_1.set('value', 'Select\nAttendance Date')
    task3_1.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task3_1.set('vertex', '1')
    task3_1.set('parent', '1')
    geo = ET.SubElement(task3_1, 'mxGeometry')
    geo.set('x', '280')
    geo.set('y', '570')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task3_1_id = cell_id
    cell_id += 1
    
    # Gateway: Choose Option
    gateway3 = ET.SubElement(root_cell, 'mxCell')
    gateway3.set('id', str(cell_id))
    gateway3.set('value', 'Mark\nOption?')
    gateway3.set('style', 'rhombus;whiteSpace=wrap;html=1;fillColor=#FFD700;strokeColor=#FFA500;strokeWidth=2')
    gateway3.set('vertex', '1')
    gateway3.set('parent', '1')
    geo = ET.SubElement(gateway3, 'mxGeometry')
    geo.set('x', '290')
    geo.set('y', '700')
    geo.set('width', '100')
    geo.set('height', '100')
    geo.set('as', 'geometry')
    gateway3_id = cell_id
    cell_id += 1
    
    # Task: Mark All Present
    task3_all = ET.SubElement(root_cell, 'mxCell')
    task3_all.set('id', str(cell_id))
    task3_all.set('value', 'Mark All\nPresent')
    task3_all.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task3_all.set('vertex', '1')
    task3_all.set('parent', '1')
    geo = ET.SubElement(task3_all, 'mxGeometry')
    geo.set('x', '80')
    geo.set('y', '880')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task3_all_id = cell_id
    cell_id += 1
    
    # Task: Select Individuals
    task3_sel = ET.SubElement(root_cell, 'mxCell')
    task3_sel.set('id', str(cell_id))
    task3_sel.set('value', 'Select\nIndividuals')
    task3_sel.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task3_sel.set('vertex', '1')
    task3_sel.set('parent', '1')
    geo = ET.SubElement(task3_sel, 'mxGeometry')
    geo.set('x', '480')
    geo.set('y', '880')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task3_sel_id = cell_id
    cell_id += 1
    
    # Task: Enter Check-in/out
    task3_2 = ET.SubElement(root_cell, 'mxCell')
    task3_2.set('id', str(cell_id))
    task3_2.set('value', 'Enter Check-in\nCheck-out Time')
    task3_2.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task3_2.set('vertex', '1')
    task3_2.set('parent', '1')
    geo = ET.SubElement(task3_2, 'mxGeometry')
    geo.set('x', '280')
    geo.set('y', '1020')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task3_2_id = cell_id
    cell_id += 1
    
    # Task: Calculate Hours
    task3_3 = ET.SubElement(root_cell, 'mxCell')
    task3_3.set('id', str(cell_id))
    task3_3.set('value', 'Calculate\nWorking Hours')
    task3_3.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task3_3.set('vertex', '1')
    task3_3.set('parent', '1')
    geo = ET.SubElement(task3_3, 'mxGeometry')
    geo.set('x', '80')
    geo.set('y', '1150')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task3_3_id = cell_id
    cell_id += 1
    
    # Task: Save Records
    task3_4 = ET.SubElement(root_cell, 'mxCell')
    task3_4.set('id', str(cell_id))
    task3_4.set('value', 'Save Attendance\nRecords')
    task3_4.set('style', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#87CEEB;strokeColor=#4682B4;strokeWidth=2')
    task3_4.set('vertex', '1')
    task3_4.set('parent', '1')
    geo = ET.SubElement(task3_4, 'mxGeometry')
    geo.set('x', '280')
    geo.set('y', '1150')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    task3_4_id = cell_id
    cell_id += 1
    
    # End Event
    end3 = ET.SubElement(root_cell, 'mxCell')
    end3.set('id', str(cell_id))
    end3.set('value', 'Attendance\nRecorded')
    end3.set('style', 'ellipse;whiteSpace=wrap;html=1;fillColor=#90EE90;strokeColor=#228B22;strokeWidth=2')
    end3.set('vertex', '1')
    end3.set('parent', '1')
    geo = ET.SubElement(end3, 'mxGeometry')
    geo.set('x', '480')
    geo.set('y', '1150')
    geo.set('width', '120')
    geo.set('height', '80')
    geo.set('as', 'geometry')
    end3_id = cell_id
    cell_id += 1
    
    # ===== CONNECTING ARROWS FOR PROCESS 1 =====
    
    # Arrow: Start -> Task 1
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(start1_id))
    arr.set('target', str(task1_1_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Arrow: Task 1 -> Task 2
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task1_1_id))
    arr.set('target', str(task1_2_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Arrow: Task 2 -> Gateway
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task1_2_id))
    arr.set('target', str(gateway1_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Arrow: Gateway -> Error (NO)
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('value', 'NO')
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF6B6B;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(gateway1_id))
    arr.set('target', str(task1_err_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Arrow: Gateway -> Task 3 (YES)
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('value', 'YES')
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#228B22;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(gateway1_id))
    arr.set('target', str(task1_3_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Arrow: Task 3 -> Task 4
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task1_3_id))
    arr.set('target', str(task1_4_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Arrow: Task 4 -> Task 5
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task1_4_id))
    arr.set('target', str(task1_5_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Arrow: Task 5 -> End OK
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#228B22;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task1_5_id))
    arr.set('target', str(end1_ok_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Arrow: Error -> End Error
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF6B6B;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task1_err_id))
    arr.set('target', str(end1_err_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # ===== CONNECTING ARROWS FOR PROCESS 2 =====
    
    # Start -> Task 1
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(start2_id))
    arr.set('target', str(task2_1_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Task 1 -> Task 2
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task2_1_id))
    arr.set('target', str(task2_2_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Task 2 -> Gateway
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task2_2_id))
    arr.set('target', str(gateway2_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Gateway -> End Error (NO)
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('value', 'NO')
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF6B6B;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(gateway2_id))
    arr.set('target', str(end2_err_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Gateway -> Task 3 (YES)
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('value', 'YES')
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#228B22;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(gateway2_id))
    arr.set('target', str(task2_3_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Task 3 -> Task 4
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task2_3_id))
    arr.set('target', str(task2_4_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Task 4 -> Gateway 2B
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task2_4_id))
    arr.set('target', str(gateway2_b_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Gateway 2B -> Approve (YES)
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('value', 'YES')
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#228B22;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(gateway2_b_id))
    arr.set('target', str(task2_approve_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Gateway 2B -> Reject (NO)
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('value', 'NO')
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF6B6B;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(gateway2_b_id))
    arr.set('target', str(task2_reject_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Approve -> Notification
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#228B22;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task2_approve_id))
    arr.set('target', str(task2_notif_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Reject -> Notification
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF6B6B;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task2_reject_id))
    arr.set('target', str(task2_notif_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Notification -> End
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#228B22;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task2_notif_id))
    arr.set('target', str(end2_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # ===== CONNECTING ARROWS FOR PROCESS 3 =====
    
    # Start -> Task 1
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(start3_id))
    arr.set('target', str(task3_1_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Task 1 -> Gateway
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task3_1_id))
    arr.set('target', str(gateway3_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Gateway -> Mark All
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('value', 'All')
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#228B22;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(gateway3_id))
    arr.set('target', str(task3_all_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Gateway -> Select Individuals
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('value', 'Individual')
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#228B22;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(gateway3_id))
    arr.set('target', str(task3_sel_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Mark All -> Task 2
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task3_all_id))
    arr.set('target', str(task3_2_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Select -> Task 2
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task3_sel_id))
    arr.set('target', str(task3_2_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Task 2 -> Task 3
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task3_2_id))
    arr.set('target', str(task3_3_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Task 3 -> Task 4
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task3_3_id))
    arr.set('target', str(task3_4_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Task 4 -> End
    arr = ET.SubElement(root_cell, 'mxCell')
    arr.set('id', str(cell_id))
    arr.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#228B22;strokeWidth=2;endArrow=block;endFill=1')
    arr.set('edge', '1')
    arr.set('parent', '1')
    arr.set('source', str(task3_4_id))
    arr.set('target', str(end3_id))
    geo = ET.SubElement(arr, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    cell_id += 1
    
    # Save XML
    xml_str = ET.tostring(root, encoding='unicode')
    
    with open('HRM_BPMN.drawio', 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<mxfile host="drawio" modified="2026-05-11" agent="Mozilla/5.0" version="16.0.0" etag="abc123">\n')
        f.write('  <diagram id="HRM-BPMN" name="HRM Business Process Model">\n')
        f.write('    ')
        f.write(xml_str)
        f.write('\n  </diagram>\n')
        f.write('</mxfile>\n')
    
    print('✓ HRM_BPMN.drawio has been created successfully!')
    print('\nBPMN Diagrams included:')
    print('\n  PROCESS 1: Employee Onboarding')
    print('    - Admin initiates creation')
    print('    - Fill form → Validate data → Decision gate')
    print('    - Create user account → Save to DB → Send welcome email')
    print('    - End: Employee onboarded OR Error notified')
    print('\n  PROCESS 2: Leave Request Workflow')
    print('    - Employee requests leave')
    print('    - Submit form → Validate dates → Decision gate')
    print('    - Set status to PENDING → Notify manager → Manager approval')
    print('    - Approve/Reject → Send notification → End: Leave processed')
    print('\n  PROCESS 3: Daily Attendance Recording')
    print('    - Admin accesses attendance page')
    print('    - Select date → Choose option (All/Individual)')
    print('    - Enter check-in/out times → Calculate hours → Save records')
    print('    - End: Attendance recorded')
    print('\nBPMN Elements used:')
    print('  ◯ Start/End events (Green circles)')
    print('  □ Tasks (Blue rectangles)')
    print('  ◇ Decision gateways (Yellow diamonds)')
    print('  → Flows with labels (YES/NO/All/Individual)')
    print('  ✓ Success path (Green arrows)')
    print('  ✗ Error path (Red arrows)')
    print('\nOpen with draw.io: https://draw.io')

if __name__ == '__main__':
    create_bpmn()
