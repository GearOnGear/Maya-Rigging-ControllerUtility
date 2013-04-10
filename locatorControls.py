"""
Curve Controller Utility

Animatable nurbsCurve Creator from Maya from versions 10.0+.

Author: Alexei Gaidachev - www.gaidachevrigs.com - gaidachevalex@gmail.com

Copyright (c) 2010 Alexei Gaidachev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""


import maya.cmds as cmds

import maya.OpenMaya as om

import sys

import string



class quickControls():


	def __init__( self, winName= 'colorWin' ):
		''' colorWinUI is all part of __init__ constructor.'''
		self.winName= winName
		self.winHeight = 290
		self.winWidth = 420
		

		self.fieldTexts=[ 'controlName',]
		self.checkBoxes=[ 'SingleController','SnapConnect' ]
		self.menuItems=[ 'None','Hierarchy','TweakHierarchy' ]
		self.connectBoxes=[ 'parent','point','rotate','scale' ]
		self.radioBoxes=[ 'parentCon','pointCon','rotateCon','scaleCon' ]
		self.locCheckBoxes=[ 'parentSelection', 'additionalGroups', 'selectionName' ]
		self.locTexts=[ 'locName' ]
		

		if cmds.windowPref( self.winName, query=True, exists=True, ):
			cmds.windowPref( self.winName, wh= ( self.winWidth, self.winHeight ),  )
			cmds.windowPref( self.winName, remove=True )
		

		if cmds.window( self.winName, q=1, ex= 1 ) == True:
			cmds.deleteUI( self.winName )

		cmds.window( self.winName, tlb=1, wh=( self.winWidth, self.winHeight ), t= "Curve Controller Utility" )
		tabs = cmds.tabLayout()
		cmds.setParent( tabs )
		child1 = cmds.rowColumnLayout( nr=3, rh= [(1, 100),( 2, 60 ),( 3, 20)])
		
		# Tab1
		cmds.frameLayout( label= 'Choose Colour :', width= 412, h=30, parent= child1 )
		cmds.rowColumnLayout( nc=3, cw= [(1, 135),( 2, 135 ),( 3, 135 )] )
		
		# Color buttons.
		cmds.button( 'purple',   l= 'Purple ',  w= 60, h=25, bgc=(0.846000000089406967,0.03,0.7839999794960022 ), aop=1, c= "cmds.color(ud=7 )" )
		cmds.button( 'red',    l= 'Red ',   w= 60, h=25, bgc=(0.85699999332427979,0.14800000190734863,0.3190000057220459 ), aop=1,c= "cmds.color(ud=8 )" )
		cmds.button( 'brown',  l= 'Brown ', w= 60, h=25, bgc=(0.602,0.452,0.173 ), aop=1, c= "cmds.color(ud=1)" )
		cmds.button( 'green',  l= 'Green ', w= 60, h=25, bgc=(0.5311,0.662,0.1 ), aop=1,c= "cmds.color(ud=3)" )
		cmds.button( 'beige', l= 'Beige ',   w= 60, h=25, bgc=(0.225,0.415,0.1 ), aop=1,c= "cmds.color(ud=2)" )
		cmds.button( 'lightGreen', l= 'LightGreen ',   w= 60, h=25, bgc=(0.0,0.668,0.268 ), aop=1,c= "cmds.color(ud=4)" )
		cmds.button( 'cyan', l= 'Cyan ',  w= 60, h=25, bgc=(0.1, 0.4, 0.5 ), aop=1,c= "cmds.color(ud=5)" )
		cmds.button( 'skyBlue', l= 'SkyBlue ',   w= 60, h=25, bgc=(0.36,0.49,0.811 ), aop=1,c= "cmds.color(ud=6 )" )

		# Create controllers.
		nameFrame= cmds.frameLayout( label= 'Name Controllers: ', width= 412, h=50, parent=child1  )

		cmds.text( "Put down 'Name' and it will result in:  Name#_ctl ", parent= nameFrame )


		for i in self.fieldTexts:
			cmds.textField( i, text= 'defaultControlName', parent= nameFrame )

		funcFrame= cmds.frameLayout( l= "Choose Function:", w=412, h= 100, parent= child1 )
		funcLabel = cmds.rowColumnLayout( numberOfColumns=4, columnWidth=[(1, 120), (2, 100), (3, 100)] )

		for i in self.checkBoxes:
			cmds.checkBox( i, parent= funcLabel )
			
		self.featureOptions = cmds.optionMenu( label='Features:' )
		for eachItem in self.menuItems:
			cmds.menuItem( label= eachItem )

		cmds.button( label= "Create Controller(s)", bgc= ( 0.05, 0.4, 0.5 ), height=30, command= self.function, parent = funcFrame )
		cmds.button( label= "Close", height=20, command= self.deleteUI, parent=funcFrame )
		
		cmds.setParent( tabs )

		# Tab2
		child2= cmds.rowColumnLayout( numberOfColumns= 2, cw= [(1, 250),( 2, 100 )], parent=tabs )
		
		# Constraint boxes.
		constraintBox= cmds.frameLayout( l= "Choice Connections:", w=206, h= 150, parent=child2 )

		cmds.radioButtonGrp( self.connectBoxes[0], numberOfRadioButtons=2, labelArray2=['parentConstraint', 'parentConnect'], sl=1 )
		cmds.radioButtonGrp( self.connectBoxes[1], numberOfRadioButtons=2, labelArray2=['pointConstraint', 'normallateConnect'], sl=1 )
		cmds.radioButtonGrp( self.connectBoxes[2], numberOfRadioButtons=2, labelArray2=['rotateConstraint', 'rotateConnect'], sl=1 )
		cmds.radioButtonGrp( self.connectBoxes[3], numberOfRadioButtons=2, labelArray2=['scaleConstraint', 'scaleConnect'], sl=1 )

		# Connection boxes.
		connectBox= cmds.frameLayout( l= "ApplyConnections:", w=206, h= 150, parent=child2 )
		for eachConnect in self.radioBoxes:
			cmds.checkBox( eachConnect,label=eachConnect, parent = connectBox )

		cmds.checkBox( self.radioBoxes[0], e=1, value=1 )
		cmds.checkBox( self.radioBoxes[3], e=1, value=1 )


		# Tab3
		child3= cmds.rowColumnLayout( numberOfColumns= 1, cw= [(1, 50)], parent=tabs )

		locFuncFrame= cmds.frameLayout( l= "Choose Name :", w=412, h= 80, parent= child3 )

		for i in self.locTexts:
			cmds.text( "Put down 'name' and you'll get 'name#_grp; " )
			cmds.text( "With selectionName: 'geo_name_grp'; Text field will be void." )
			cmds.textField( i, text='defaultGroupName', parent= locFuncFrame )


		locFrame= cmds.frameLayout( l= "Create Locator(s) with function(s):", w=412, h= 120, parent= child3 )
		locFuncLabel = cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 150), (2, 150), (2, 150) ] )

		for i in self.locCheckBoxes:
			cmds.checkBox( i, parent= locFuncLabel )


		cmds.text( "Choose normalforms or vertices, click button to create a locator.", parent=locFrame )
		cmds.button( label= "Create Locator(s)", bgc= ( 0.5, 0.4, 0.5 ), height=40, command= self.locators, parent = locFrame )




		cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Controllers'), (child2, 'snapConnections'), (child3, 'Locators') ) )
		cmds.tabLayout( tabs, edit=True, selectTabIndex=1 )



		cmds.showWindow(self.winName)
		cmds.window(self.winName, edit= True, wh=[self.winWidth,self.winHeight])



	def deleteUI(self, *args):
		''' Deletes colorWin UI. '''

		#if cmds.windowPref( self.winName, query=True, exists=True, ):
			#cmds.windowPref( self.winName, remove=True )

		if cmds.window( 'colorWin', query= True, exists= True ):
			cmds.deleteUI( 'colorWin' )
			print "GLaDOS says: 'Goodbye.'"


			
	def locators(self, *args):
		''' Locator(s) function. Independent from the __init__ module. '''

		selection= cmds.ls( sl=True, fl=True )

		parentSelection = cmds.checkBox( self.locCheckBoxes[0], value= True, query= True )
		addAdditionalGroups = cmds.checkBox( self.locCheckBoxes[1], value= True, query= True )
		selNaming = cmds.checkBox( self.locCheckBoxes[2], value= True, query= True )
		alpha = string.uppercase
		object= []
		locators= []

		AboveAlphabet = False
		vtxSel = False

		if not selection:
			om.MGlobal.displayWarning('Please select a normalform object or a vertex component.')
			sys.exit()


		if selNaming == False:
			locName = cmds.textField( self.locTexts, query= True, tx=1 )

			if not locName:
				om.MGlobal.displayWarning('Cannot have an empty text field!.')
				sys.exit()


			

		print '---------------------------------------------'

		try:

			if selection[0].split('.')[1].split('[')[0] == 'vtx':
				print 'Selection is a vertex.'

				object = selection[0].split('.')[0]
	
				if selNaming == True:
					locName= 'geo_%s_grp'%selection[0].split('.')[0]

	
				vtxSel = True

		except:

			pass

		if cmds.nodeType(selection[0]) == 'normalform':
			print 'Selection is a normalform.'

		if addAdditionalGroups == True:
			print 'Adding additional groups:  %s'%addAdditionalGroups

		if selNaming == True:
			print 'Use naming from selection:  %s'%selNaming

		if selNaming == False:
			print 'Use naming from textField:  %s'%selNaming

		if parentSelection == True:
			print 'Parenting selections:  %s'%parentSelection


		# Create locators in the center of geos.
		if vtxSel == False:

			if (len( selection ) < 26) == True:
				AboveAlphabet = False
				print "%s is greater than 25: %s"%( len(selection), AboveAlphabet)
	
			if (len( selection ) > 26) == True:
				AboveAlphabet = True
				print "%s is greater than 26: %s"%( len(selection), AboveAlphabet)



			for index, eachSel in enumerate(selection):
				

				if cmds.getAttr( '%s.tx'%eachSel, k=0, l=1 ):

					cmds.setAttr( '%s.tx'%eachSel, k=1, l=0 )
					cmds.setAttr( '%s.ty'%eachSel, k=1, l=0 )
					cmds.setAttr( '%s.tz'%eachSel, k=1, l=0 )

				if cmds.getAttr( '%s.tx'%eachSel, k=1, l=0 ):

					# Alphabet has 26 letters. If selection is > 26, do numbers.
					if selNaming == True:

						locName = eachSel

						if "_grp" in eachSel:
							locName.replace( "_grp", "" )


						if "_GRP" in eachSel:
							locName.replace( "_GRP", "" )


						if "_GP" in eachSel:
							locName.replace( "_GP", "" )

						if "_gp" in eachSel:
							locName.replace( "_gp", "" )


						if AboveAlphabet == False:
							point= cmds.spaceLocator( name= '%s%s_grp'%( locName, alpha[index] ) )

						if AboveAlphabet == True:
							point= cmds.spaceLocator( name= '%s%s_grp'%( locName, index ) )



					if selNaming == False:



						if AboveAlphabet == False:
							point= cmds.spaceLocator( name= '%s%s_grp'%( locName, alpha[index] ) )

						if AboveAlphabet == True:
							point= cmds.spaceLocator( name= '%s%s_grp'%( locName, index ) )
					

					cmds.align( point, eachSel, xAxis='mid', yAxis='mid', zAxis='mid', atl=True )

					print 'Created a locator for: %s'%eachSel


				if addAdditionalGroups == True:

					rename = point[0].replace( "_grp", "" )
					dupl= cmds.duplicate( point, name = rename + '_plug' )

					cmds.select(clear=True)
					originGrp= cmds.group( name= '%s_zro'%rename, em=True, world=True )
					cmds.parent( originGrp, dupl )

					cmds.delete( cmds.listRelatives( dupl, shapes=True )[0] )

					cmds.parent( dupl, point )


				if parentSelection == True:

					if addAdditionalGroups == False:
						cmds.parent( eachSel, point )

					if addAdditionalGroups == True:
						cmds.parent( eachSel, originGrp )


				locators.append( point )

			cmds.select(clear=True)
			for eachLoc in locators:
				cmds.select( eachLoc, tgl=True )

			# End of len(selection) function of locator method.
			print '---------------------------------------------'
			
		
		# Create locators with aim constrained towards a vertex.
		if vtxSel == True:

			if len(selection) == 1:

				vertexA= selection[0].split('.')[1].split('[')[1].split(']')[0].split(':')[0]
				print selection[0].split('.')[0] + '.vtx[%s]'%vertexA

				Target0= cmds.xform( selection[0].split('.')[0] + '.vtx[%s]'%vertexA, translation=True, worldSpace=True, query=True )

				point= cmds.spaceLocator( name= locName )

				cmds.xform( point, translation= Target0 )

				if addAdditionalGroups == True:

					rename = point[0].replace( "_grp", "" )
					dupl= cmds.duplicate( point, name = rename + '_plug' )

					cmds.select(clear=True)
					originGrp= cmds.group( name= '%s_zro'%rename, em=True, world=True )
					cmds.parent( originGrp, dupl )

					cmds.delete( cmds.listRelatives( dupl, shapes=True )[0] )

					cmds.parent( dupl, point )


				if parentSelection == True:

					if addAdditionalGroups == False:
						cmds.parent( object, point )

					if addAdditionalGroups == True:
						cmds.parent( object, originGrp )

					cmds.select( point )


				print( ' Created a locator on a vertex:  %s'%selection[0].split('.')[1] )


			if len(selection) == 2:

				start= cmds.spaceLocator( name='start_placer_loc' )
				end= cmds.spaceLocator( name='end_placer_loc' )

				point= cmds.spaceLocator( name= locName )

				locList= cmds.ls( start, end )

				target0= cmds.xform( selection[0], translation=True, worldSpace=True, query=True )
				target1= cmds.xform( selection[1], translation=True, worldSpace=True, query=True )

				cmds.xform( start, ws=1, t= target0 )
				cmds.xform( end, ws=1, t= target1 )

				cmds.pointConstraint( start, end, point, maintainOffset=False )
				cmds.aimConstraint( start, point, maintainOffset=False )


				cmds.delete(start, end)


				if addAdditionalGroups == True:

					rename = point[0].replace( "_grp", "" )
					dupl= cmds.duplicate( point, name = rename + '_plug' )

					cmds.select(clear=True)
					originGrp= cmds.group( name= '%s_zro'%rename, em=True, world=True )
					cmds.parent( originGrp, dupl )

					cmds.delete( cmds.listRelatives( dupl, shapes=True )[0] )

					cmds.parent( dupl, point )


				if parentSelection == True:

					if addAdditionalGroups == False:
						cmds.parent( object, point )

					if addAdditionalGroups == True:
						cmds.parent( object, originGrp )

					cmds.select( point )



			if len(selection) > 2:

				# Credit: Marc English for the boundingbox.
				point= cmds.spaceLocator( name= locName )


				bbox =  cmds.exactWorldBoundingBox(selection)	

				x = (bbox[0] + bbox[3]) / 2	
				y = (bbox[1] + bbox[4]) / 2	
				z = (bbox[2] + bbox[5]) / 2


				cmds.setAttr( point ,x,y,z)


				if addAdditionalGroups == True:

					rename = point[0].replace( "_grp", "" )
					dupl= cmds.duplicate( point, name = rename + '_plug' )

					cmds.select(clear=True)
					originGrp= cmds.group( name= '%s_zro'%rename, em=True, world=True )
					cmds.parent( originGrp, dupl )

					cmds.delete( cmds.listRelatives( dupl, shapes=True )[0] )

					cmds.parent( dupl, point )


				if parentSelection == True:

					if addAdditionalGroups == False:
						cmds.parent( object, point )

					if addAdditionalGroups == True:
						cmds.parent( object, originGrp )

					cmds.select( point )


			print( ' Created a locator between two vertices:  %s'%point )

			print '---------------------------------------------'



	def variables( self, *args ):
		''' Creates variables needed. Error checking. '''

		self.index = ['1']
		self.checkBoxes
		self.fieldTexts
		self.name = cmds.textField( self.fieldTexts, query= True, tx=1 )
		self.alpha = [chr(a) for a in xrange(ord("A"), ord("Z")+1)]

		# connectBoxes.
		self.parentCon= cmds.checkBox( self.radioBoxes[0], q=1, value=1 )
		self.pointCon= cmds.checkBox( self.radioBoxes[1], q=1, value=1 )
		self.rotateCon= cmds.checkBox( self.radioBoxes[2], q=1, value=1 )
		self.scaleCon= cmds.checkBox( self.radioBoxes[3], q=1, value=1 )


		# RadioButtons.
		self.parent= cmds.radioButtonGrp( self.connectBoxes[0], query=1, sl=1 )
		self.point= cmds.radioButtonGrp( self.connectBoxes[1], query=1, sl=1 )
		self.rotate= cmds.radioButtonGrp( self.connectBoxes[2], query=1, sl=1 )
		self.scale= cmds.radioButtonGrp( self.connectBoxes[3], query=1, sl=1 )

		if self.parentCon == True:
			if self.pointCon == True:
				om.MGlobal.displayWarning( 'You cannot do a Parent and a Point connection.' )
				sys.exit()
			if self.rotateCon == True:
				om.MGlobal.displayWarning( 'You cannot do a Parent and a Rotate connection.' )
				sys.exit()

		#	Checks to see if the text is blank.
		if not self.name:
			om.MGlobal.displayWarning( 'Text is not valid in an empty text field.' )
			sys.exit()

		#	Single controller function.
		self.chexBox= cmds.checkBox( self.checkBoxes[0], value= True, query= True )

		#	Snapping function.
		self.snapBox= cmds.checkBox( self.checkBoxes[1], value= True, query= True )

		#	Chooses special option.
		self.option = cmds.optionMenu( self.featureOptions, q=1, v=1 )
		



		self.grpList= [ ]
		self.ctlList= [ ]
		self.ctlShapeList= [ ]
		self.cirlceHistoryList= []
		self.scaleList= ['.sx','.sy','.sz' ]
		self.channelList= [ '.sx','.sy','.sz','.v' ]
		self.grpChannel= [ '.sx','.sy','.sz','.v','.tx','.ty','.tz','.rx','.ry','.rz' ]
		self.mdnChannel= [ '.i1x','.i1y','.i1z','.i2x','.i2y','.i2z' ]
		self.newChannel= [ 'localRotationX','localRotationY','localRotationZ' ]
		self.selection= cmds.ls(sl=1)

		self.AboveAlphabet= []

		# Parenting hirearchy.
		self.relevantControls= []
		self.relevantGroups= []
		
		#	If snapping enabled, proceed for error checking.
		if self.snapBox == True:

			#	Checks to see if the selection is greater than three for special option 2.
			if len(self.selection) < 3:
				if self.option == 2:
					om.MGlobal.displayWarning( "You must have at least three selected components." )
					sys.exit()
			
			#	If there is no selection, return a warning.
			if not self.selection:
				om.MGlobal.displayWarning( 'Nothing is selected.' )
				sys.exit()

			#	Checks if selection == 'normalform, joint or a clusterHandle.' If not, return a warning.
			if self.selection:
				for each in self.selection:
					child = cmds.listRelatives( each, ad=1, c=1 )

					if not child:
						child=each
					
					self.selectionType = cmds.objectType( each )

					#if not self.selectionType == [ 'transform', 'joint', 'clusterHandle', 'ikHandle' ]:
						#om.MGlobal.displayWarning( 'Your selection must be a transform, joint or a clusterHandle.' )
						#sys.exit()

		if self.snapBox == False:
			if self.option == self.menuItems[1] or self.option == self.menuItems[2]:
				om.MGlobal.displayWarning( 'You cannot have a hirearchial FK for one controller. snapConnect Must be checked on.' )
				sys.exit()

		#	Prints the shit.
		print '---------------------------------------------'
		print 'Creating single controllers:  %s'%self.chexBox
		print 'Snap enabled:  %s'%self.snapBox
		
		print 'Feature: %s'%self.option

		if (len( self.selection ) < 26) == True:
			self.AboveAlphabet = False
			print "%s is greater than 25: %s"%( len(self.selection), self.AboveAlphabet)

		if (len( self.selection ) > 26) == True:
			self.AboveAlphabet = True
			print "%s is greater than 26: %s"%( len(self.selection), self.AboveAlphabet)

		if self.snapBox == True:


			if self.selection:
				if self.parentCon == True:
					if self.parent == 1:
						print 'parentConstraining to:   %s'%self.selection
					if self.parent == 2:
						print " 'parent' DirectConnecting to:   %s"%self.selection

				if self.pointCon == True:
					if self.parent == 1:
						print 'pointConstraining to:   %s'%self.selection
					if self.parent == 2:
						print "normallateConnecting to:   %s"%self.selection

				if self.rotateCon == True:
					if self.parent == 1:
						print 'orientConstraining to:   %s'%self.selection
					if self.parent == 2:
						print "rotateConnecting to:   %s"%self.selection

				if self.scaleCon == True:
					if self.parent == 1:
						print 'scaleConstraining to:   %s'%self.selection
					if self.parent == 2:
						print "scaleConnecting to:   %s"%self.selection


		print '---------------------------------------------'


	def createControl(self, *args ):
		''' Creates a single Controller '''

		if self.AboveAlphabet == False:

			nurbCircle= cmds.circle( name= self.name + '%s_ctl'%self.eachAlpha )
			self.ctl= nurbCircle[0]
			cirlceHistory= nurbCircle[1]
			ctlShape= cmds.listRelatives( self.ctl, children=1 )[0]
			
			grpA= cmds.group( self.ctl, name= self.name + '%s_ctl_cnst'%self.eachAlpha )
			grpZro= cmds.group( grpA, name= self.name + '%s_zro'%self.eachAlpha )
			grpPlug= cmds.group( grpZro, name= self.name + '%s_plug'%self.eachAlpha )
			self.grpC= cmds.group( grpPlug, name= self.name + '%s_grp'%self.eachAlpha )

		if self.AboveAlphabet == True:

			nurbCircle= cmds.circle( self.name + '%s_ctl'%self.index )
			self.ctl= nurbCircle[0]
			cirlceHistory= nurbCircle[1]
			ctlShape= cmds.listRelatives( self.ctl, children=1 )[0]
			
			grpA= cmds.group( self.ctl, name= self.name + '%s_ctl_cnst'%self.index )
			grpZro= cmds.group( grpA, name= self.name + '%s_zro'%self.index )
			grpPlug= cmds.group( grpZro, name= self.name + '%s_plug'%self.index )
			self.grpC= cmds.group( grpPlug, name= self.name + '%s_grp'%self.index )

		self.ctlList.append( self.ctl )
		self.grpList.append( self.grpC )
		self.cirlceHistoryList.append( cirlceHistory )
		self.ctlShapeList.append( ctlShape )

		cmds.addAttr( self.ctl, ln='globalScale',at='float', min=0, dv=1 )
		cmds.setAttr( self.ctl + '.globalScale',  k=1 )

		for each in self.scaleList:
			cmds.connectAttr( self.ctl + '.globalScale', self.ctl + each )
		for each in self.channelList:
			cmds.setAttr( self.ctl + each, lock=1, k=0 )
		
		# Radius.
		cmds.addAttr( ctlShape, ln='radius', at='float', min=0, dv=1 )
		cmds.setAttr( '%s.radius'%ctlShape, k=1, lock=0, channelBox=1 )

		cmds.connectAttr( '%s.radius'%ctlShape, '%s.radius'%cirlceHistory )


		# Center Shape Offsets..
		cmds.addAttr( ctlShape, ln='centerX', at='float', dv=0 )
		cmds.setAttr( '%s.centerX'%ctlShape, k=1, lock=0, channelBox=1 )
		cmds.addAttr( ctlShape, ln='centerY', at='float', dv=0 )
		cmds.setAttr( '%s.centerY'%ctlShape, k=1, lock=0, channelBox=1 )
		cmds.addAttr( ctlShape, ln='centerZ', at='float', dv=0 )
		cmds.setAttr( '%s.centerZ'%ctlShape, k=1, lock=0, channelBox=1 )
		cmds.connectAttr( '%s.centerX'%ctlShape, '%s.centerX'%cirlceHistory )
		cmds.connectAttr( '%s.centerY'%ctlShape, '%s.centerY'%cirlceHistory )
		cmds.connectAttr( '%s.centerZ'%ctlShape, '%s.centerZ'%cirlceHistory )

		# Normals Shape Offsets..
		cmds.addAttr( ctlShape, ln='normalX', at='float', dv=1 )
		cmds.setAttr( '%s.normalX'%ctlShape, k=1, lock=0, channelBox=1 )
		cmds.addAttr( ctlShape, ln='normalY', at='float', dv=0 )
		cmds.setAttr( '%s.normalY'%ctlShape, k=1, lock=0, channelBox=1 )
		cmds.addAttr( ctlShape, ln='normalZ', at='float', dv=0 )
		cmds.setAttr( '%s.normalZ'%ctlShape, k=1, lock=0, channelBox=1 )
		cmds.connectAttr( '%s.normalX'%ctlShape, '%s.normalX'%cirlceHistory )
		cmds.connectAttr( '%s.normalY'%ctlShape, '%s.normalY'%cirlceHistory )
		cmds.connectAttr( '%s.normalZ'%ctlShape, '%s.normalZ'%cirlceHistory )

		
		# Degree // resolution << Naming conflict
		cmds.addAttr( ctlShape, ln='resolution', at='float', dv=0, min=0, max=1 )
		cmds.setAttr( '%s.resolution'%ctlShape, k=1, lock=0, channelBox=1 )
		cmds.connectAttr( '%s.resolution'%ctlShape, '%s.degree'%cirlceHistory )

		# Sweep
		cmds.addAttr( ctlShape, ln='sweep', at='float', dv=360, min=0, max=360 )
		cmds.setAttr( '%s.sweep'%ctlShape, k=1, lock=0, channelBox=1 )
		cmds.connectAttr( '%s.sweep'%ctlShape, '%s.sweep'%cirlceHistory )

		
		# Sections
		cmds.addAttr( ctlShape, ln='sections', at='float', dv=1, min=0 )
		cmds.setAttr( '%s.sections'%ctlShape, k=1, lock=0, channelBox=1 )
		cmds.connectAttr( '%s.sections'%ctlShape, '%s.sections'%cirlceHistory )

		# Renames circle history.
		if self.AboveAlphabet == False:
			cmds.rename( cirlceHistory, 'HISTORY%s%s_ctl'%( self.name, self.eachAlpha ) )
		
		if self.AboveAlphabet == True:
			cmds.rename( cirlceHistory, 'HISTORY%s%s_ctl'%( self.name, self.index  ) )
			
		# Locking uneeded channels upon connection choice.
		if self.scaleCon == False:
			cmds.setAttr( '%s%s'%( self.ctl, '.globalScale' ), lock = False, keyable = False )


	def createLayerControl(self, *args ):
		''' Creates multiLayeredControllers. '''
		self.grpList= []
		self.ctlShapeList= []
		self.ctlList= []
		self.cirlceHistoryList= []

		
		for i in range(3):

			nurbCircle= cmds.circle( name= self.name + '%s%s_ctl'%( self.index + 1, self.alpha[i] ) )
			ctl= nurbCircle[0]
			ctlShape= cmds.listRelatives( ctl, children= 1 )[0]
			__cirlceHistory= nurbCircle[1]
			cirlceHistory= cmds.rename( __cirlceHistory, 'HISTORY%s%s%s_ctl'%( self.name, self.index + 1, self.alpha[i] ) )

			#print ctl
			grpA= cmds.group( ctl, name= self.name + '%s%s_ctl_cnst'%( self.index + 1, self.alpha[i] ) )
			grpZro= cmds.group( grpA, name= self.name + '%s%s_zro'%( self.index + 1, self.alpha[i] ) )
			grpPlug= cmds.group( grpZro, name= self.name + '%s%s_plug'%( self.index + 1, self.alpha[i] ) )
			grpB= cmds.group( grpPlug, name= self.name + '%s%s_grp'%( self.index + 1, self.alpha[i] ) )

			self.ctlList.append( ctl )
			self.grpList.append( grpB )
			self.ctlShapeList.append( ctlShape )
			self.cirlceHistoryList.append( cirlceHistory )
			
			cmds.addAttr( ctl, ln='globalScale',at='float', min=0, dv=1 )
			cmds.setAttr( ctl + '.globalScale',  k=1 )

			for each in self.scaleList:
				cmds.connectAttr( ctl + '.globalScale', ctl + each )
			for each in self.channelList:
				cmds.setAttr( ctl + each, lock=1, k=0 )

		# Center Shape Offsets.
		cmds.addAttr( self.ctlShapeList[0], ln='centerX', at='float', min=0, dv=0 )
		cmds.setAttr( '%s.centerX'%self.ctlShapeList[0], k=1, lock=0, channelBox=1 )
		cmds.addAttr( self.ctlShapeList[0], ln='centerY', at='float', min=0, dv=0 )
		cmds.setAttr( '%s.centerY'%self.ctlShapeList[0], k=1, lock=0, channelBox=1 )
		cmds.addAttr( self.ctlShapeList[0], ln='centerZ', at='float', min=0, dv=0 )
		cmds.setAttr( '%s.centerZ'%self.ctlShapeList[0], k=1, lock=0, channelBox=1 )
		cmds.connectAttr( '%s.centerX'%self.ctlShapeList[0], '%s.centerX'%self.cirlceHistoryList[0] )
		cmds.connectAttr( '%s.centerY'%self.ctlShapeList[0], '%s.centerY'%self.cirlceHistoryList[0] )
		cmds.connectAttr( '%s.centerZ'%self.ctlShapeList[0], '%s.centerZ'%self.cirlceHistoryList[0] )

		# Normals Shape Offsets.
		cmds.addAttr( self.ctlShapeList[0], ln='normalX', at='float', dv=0 )
		cmds.setAttr( '%s.normalX'%self.ctlShapeList[0], k=1, lock=0, channelBox=1 )
		cmds.addAttr( self.ctlShapeList[0], ln='normalY', at='float', dv=0 )
		cmds.setAttr( '%s.normalY'%self.ctlShapeList[0], k=1, lock=0, channelBox=1 )
		cmds.addAttr( self.ctlShapeList[0], ln='normalZ', at='float', dv=0 )
		cmds.setAttr( '%s.normalZ'%self.ctlShapeList[0], k=1, lock=0, channelBox=1 )
		cmds.connectAttr( '%s.normalX'%self.ctlShapeList[0], '%s.normalX'%self.cirlceHistoryList[0] )
		cmds.connectAttr( '%s.normalY'%self.ctlShapeList[0], '%s.normalY'%self.cirlceHistoryList[0] )
		cmds.connectAttr( '%s.normalZ'%self.ctlShapeList[0], '%s.normalZ'%self.cirlceHistoryList[0] )

		# Radius.
		cmds.addAttr( self.ctlShapeList[0], ln='radius', at='float', dv=1, min=0 )
		cmds.setAttr( '%s.radius'%self.ctlShapeList[0], k=1, lock=0, channelBox=1 )
		cmds.connectAttr( '%s.radius'%self.ctlShapeList[0], '%s.radius'%self.cirlceHistoryList[0] )

		# Degree >> resolution << Naming conflict.
		cmds.addAttr( self.ctlShapeList[0], ln='resolution', at='float', dv=0, min=0, max=1 )
		cmds.setAttr( '%s.resolution'%self.ctlShapeList[0], k=1, lock=0, channelBox=1 )
		cmds.connectAttr( '%s.resolution'%self.ctlShapeList[0], '%s.degree'%self.cirlceHistoryList[0] )

		# Sweep.
		cmds.addAttr( self.ctlShapeList[0], ln='sweep', at='float', dv=360 , min=0, max=360 )
		cmds.setAttr( '%s.sweep'%self.ctlShapeList[0], k=1, lock=0, channelBox=1 )
		cmds.connectAttr( '%s.sweep'%self.ctlShapeList[0], '%s.sweep'%self.cirlceHistoryList[0] )

		# Adds controlB, controlC VIS attributes.
		cmds.addAttr( self.ctlList[0], ln='controlB', at='float', min=0, max=1, dv=0, hidden=0 )
		cmds.setAttr( self.ctlList[0] + '.controlB', k=1 )
		cmds.addAttr( self.ctlList[0], ln='controlC',at='float', min=0, max=1, dv=0, hidden=0)
		cmds.setAttr( self.ctlList[0] + '.controlC', k=1 )
		cmds.connectAttr( self.ctlList[0] + '.controlB', self.ctlShapeList[1] + '.visibility' )
		cmds.connectAttr( self.ctlList[0] + '.controlC', self.ctlShapeList[2] + '.visibility' )
		
		# Adds a MultiplyDivide node to offset the radius values on the controlB, controlC.
		MDNb= cmds.createNode( 'multiplyDivide',name= self.name + '%iB_mdn'%( self.index + 1 ) )
		MDNc= cmds.createNode( 'multiplyDivide',name= self.name + '%iC_mdn'%( self.index + 1 ) )
		cmds.connectAttr( self.ctlShapeList[0] + '.radius', MDNb + '.input1X' )
		cmds.connectAttr( self.ctlShapeList[0] + '.radius', MDNc + '.input1X' )
		cmds.connectAttr( MDNb + '.outputX', self.cirlceHistoryList[1] + '.radius' )
		cmds.connectAttr( MDNc + '.outputX', self.cirlceHistoryList[2] + '.radius' )

		for i in range( 3, 6 ):
			cmds.setAttr( MDNb + self.mdnChannel[i], 0.75 )
			cmds.setAttr( MDNc + self.mdnChannel[i], 0.50 )

		# propagate the attributes to the coltrolB, controlC.
		# Centers.
		cmds.connectAttr( self.ctlShapeList[0] + '.centerX', self.cirlceHistoryList[1] + '.centerX' )
		cmds.connectAttr( self.ctlShapeList[0] + '.centerY', self.cirlceHistoryList[1] + '.centerY' )
		cmds.connectAttr( self.ctlShapeList[0] + '.centerZ', self.cirlceHistoryList[1] + '.centerZ' )
		cmds.connectAttr( self.ctlShapeList[0] + '.centerX', self.cirlceHistoryList[2] + '.centerX' )
		cmds.connectAttr( self.ctlShapeList[0] + '.centerY', self.cirlceHistoryList[2] + '.centerY' )
		cmds.connectAttr( self.ctlShapeList[0] + '.centerZ', self.cirlceHistoryList[2] + '.centerZ' )
	
		# Normals
		cmds.connectAttr( self.ctlShapeList[0] + '.normalX', self.cirlceHistoryList[1] + '.normalX' )
		cmds.connectAttr( self.ctlShapeList[0] + '.normalY', self.cirlceHistoryList[1] + '.normalY' )
		cmds.connectAttr( self.ctlShapeList[0] + '.normalZ', self.cirlceHistoryList[1] + '.normalZ' )
		cmds.connectAttr( self.ctlShapeList[0] + '.normalX', self.cirlceHistoryList[2] + '.normalX' )
		cmds.connectAttr( self.ctlShapeList[0] + '.normalY', self.cirlceHistoryList[2] + '.normalY' )
		cmds.connectAttr( self.ctlShapeList[0] + '.normalZ', self.cirlceHistoryList[2] + '.normalZ' )
	
		# Resolutions
		cmds.connectAttr( self.ctlShapeList[0] + '.sweep', self.cirlceHistoryList[1] + '.degree' )
		cmds.connectAttr( self.ctlShapeList[0] + '.sweep', self.cirlceHistoryList[2] + '.degree' )
	
		# Sweep.
		cmds.connectAttr( self.ctlShapeList[0] + '.sweep', self.cirlceHistoryList[1] + '.sweep' )
		cmds.connectAttr( self.ctlShapeList[0] + '.sweep', self.cirlceHistoryList[2] + '.sweep' )
		
		# Parents the respective controllers under the respective _cnst groups.
		cmds.parent( self.grpList[1], self.ctlList[0] )
		cmds.parent( self.grpList[2], self.ctlList[1] )

		for each in self.grpChannel:
			cmds.setAttr( self.grpList[1] + each, lock=1, k=0 )
			cmds.setAttr( self.grpList[2] + each, lock=1, k=0 )

		
		# Locking uneeded channels upon connection choice.
		if self.scaleCon == False:
			cmds.setAttr( '%s%s'%( self.ctlList[0], '.globalScale' ), lock = False, keyable = False )




	def nameBuffer( self, *args ):
		''' Name offset if the controller name exists in scene. '''
		import re
		
		alphaDict = {}
		for i, each in enumerate( string.ascii_uppercase ):
			alphaDict[i] = [each]
		

			# Finds the next letter, number in the alphabet Single controllers:
			if self.chexBox == True:
				
				if self.AboveAlphabet == True:
					if cmds.ls( '{0}*_ctl'.format( self.name ) ) != []:
						
						# only numbers:
						_findAllSingleControllers = cmds.ls( '{0}*_ctl'.format( self.name ) )[-1]
						numbers = re.search( '[0-9]+', _findAllSingleControllers ) # or this: m = re.search('\d+', myStr)
						self.index = int(numbers.group()) + 1
						self.index
						return self.index
					
				if self.AboveAlphabet == False:
					#	Checks name clashes.
					if cmds.ls( '{0}*_ctl'.format( self.name ) ) != []:
						
						findAllSingleControllers = cmds.ls( '{0}*_ctl'.format( self.name ) )[-1]
						
						alphaDict = {}
						for i, each in enumerate( string.ascii_uppercase ):
							alphaDict[each] = i
							
						letter= findAllSingleControllers.split(self.name)[1].split('_ctl')[0]
						alphaDict[letter]
						
						_copyDict = dict([(v, k) for (k, v) in alphaDict.iteritems()])
						
						# if the value goes above the alphabet. raiseError.
						if alphaDict[_copyDict[alphaDict[letter]]] == 25:
							om.MGlobal.displayWarning( 'End of alphabet reached! Ending operation.' )
							sys.exit()
						
						_alpha = _copyDict[alphaDict[letter]+1]
						
						self.eachAlpha = _alpha
						
						return self.eachAlpha
				
					if cmds.ls( '{0}*_ctl'.format( self.name ) ) == []:
						self.eachAlpha = 'A'
				
			# Multi-Layered controllers:
			if self.chexBox == False:
					#	Checks name clashes.
	
					if cmds.ls( '{0}*_ctl'.format( self.name ) ) != []:
						# only numbers:
						findAllMultilayerControllers = cmds.ls( '{0}*_ctl'.format( self.name ) )[-1]
						numbers = re.search( '[0-9]+', findAllMultilayerControllers ) # or this: m = re.search('\d+', myStr)
						self.index = int(numbers.group())
						
						return self.index

			

	def constraints( self, control, eachSel ):
		''' Constraints or connections queried. '''
		
		# Connection: ----- parent.
		if self.parentCon == True:
			if self.parent == 1:
				cmds.parentConstraint(  control, eachSel, mo=0 )

			if self.parent == 2:
				cmds.connectAttr( '%s%s'%(  control, '.tx' ), '%s%s'%( eachSel, '.tx' ) )
				cmds.connectAttr( '%s%s'%(  control, '.ty' ), '%s%s'%( eachSel, '.ty' ) )
				cmds.connectAttr( '%s%s'%(  control, '.tz' ), '%s%s'%( eachSel, '.tz' ) )
				cmds.connectAttr( '%s%s'%(  control, '.rx' ), '%s%s'%( eachSel, '.rx' ) )
				cmds.connectAttr( '%s%s'%(  control, '.ry' ), '%s%s'%( eachSel, '.ry' ) )
				cmds.connectAttr( '%s%s'%(  control, '.rz' ), '%s%s'%( eachSel, '.rz' ) )

		# Connection: ----- point.
		if self.pointCon == True:
			if self.parent == 1:
				cmds.pointConstraint(  control, eachSel, mo=0 )

			if self.parent == 2:
				cmds.connectAttr( '%s%s'%(  control, '.tx' ), '%s%s'%( eachSel, '.tx' ) )
				cmds.connectAttr( '%s%s'%(  control, '.ty' ), '%s%s'%( eachSel, '.ty' ) )
				cmds.connectAttr( '%s%s'%(  control, '.tz' ), '%s%s'%( eachSel, '.tz' ) )

		# Connection: ----- rotate.
		if self.rotateCon == True:
			if self.rotate == 1:
				cmds.orientConstraint(  control, eachSel, mo=0 )

			if self.rotate == 2:
				cmds.connectAttr( '%s%s'%(  control, '.rx' ), '%s%s'%( eachSel, '.rx' ) )
				cmds.connectAttr( '%s%s'%(  control, '.ry' ), '%s%s'%( eachSel, '.ry' ) )
				cmds.connectAttr( '%s%s'%(  control, '.rz' ), '%s%s'%( eachSel, '.rz' ) )

		# Connection: ----- scale.
		if self.scaleCon == True:
			if self.scale == 1:
				cmds.scaleConstraint(  control, eachSel, mo=0 )

			if self.scale == 2:
				cmds.connectAttr( '%s%s'%(  control, '.sx' ), '%s%s'%( eachSel, '.sx' ) )
				cmds.connectAttr( '%s%s'%(  control, '.sy' ), '%s%s'%( eachSel, '.sy' ) )
				cmds.connectAttr( '%s%s'%(  control, '.sz' ), '%s%s'%( eachSel, '.sz' ) )
				
				

	def hierarchy( self, *args ):
		''' Hirearchial controller construction. '''

		if self.chexBox == True:

			if self.option == self.menuItems[1]:

				if self.lastCreatedControl != None:

					cmds.parent( self.grpC, self.lastCreatedControl )
	
				self.lastCreatedControl = self.ctl


		if self.chexBox == False:
			
			if self.option == self.menuItems[1]:

				if self.lastCreatedControl != None:

					cmds.parent( self.grpList[0], self.lastCreatedControl )
					print "parenting %s to %s"%( self.grpList[0], self.lastCreatedControl )	

				self.lastCreatedControl = self.ctlList[2]


	def tweakHiearchy(self, eachGrp, control, position, eachSel ):
			''' Tweakable Hierarchy. '''

			self.twkGrp= []
			self.trgtGrp= []
			# Checks to see if tweakable hierarchy is set.
			if self.option == self.menuItems[2]:
				
				if self.lastCreatedControl != None:

					__controlXform= cmds.xform( self.lastCreatedControl, ws=1, m= True , q=1)
					
					# Creates _twk group and positions it for each selected.
					__twkGrpName= control.replace( "_ctl", "_twk" )
					__trgtGrpName= control.replace( "_ctl", "_trgt" )
					
					self.twkGrp= cmds.group( name= __twkGrpName, em=1  )
					self.trgtGrp= cmds.group( name= __trgtGrpName, em=1 )


					cmds.xform( self.twkGrp, ws=1, m= __controlXform )
					cmds.xform( self.trgtGrp, ws=1, m= position )
					
					# Parents each created controller's group, the target group to tweak group.
					cmds.parent( eachGrp, self.trgtGrp, self.twkGrp )
					
					#cmds.pointConstraint( self.lastCreatedControl, eachSel, mo=0 )
					#print self.lastCreatedControl, '>>>>', eachSel
					
					cmds.orientConstraint( self.trgtGrp, eachSel, mo=0 )
					cmds.orientConstraint( self.lastCreatedControl,self.twkGrp  )
					
					# Stores the last created control for next operation in the class.
					self.lastCreatedControl= control

				
				if self.lastCreatedControl == None:
					
					baseControl= []
				
					__trgtGrpName= control.replace( "_ctl", "_trgt" )
					self.trgtGrp= cmds.group( name= __trgtGrpName, em=1 )
					
					
					baseControl= cmds.xform( control, ws=1, m=True, query=True )
					cmds.xform( self.trgtGrp, ws=1, m= baseControl )
					
					cmds.parent( self.trgtGrp, control )
					
					cmds.orientConstraint( control, eachSel, mo=0 )
					
					self.lastCreatedControl= control

				self.lastCreatedtwkGrp.append( self.twkGrp )
				self.lastCreatedtrgtGrp.append( self.trgtGrp )

				if len( self.selection ) == len( self.lastCreatedtrgtGrp ):
					for eachTweak, eachTarget in zip( self.lastCreatedtwkGrp[1:], self.lastCreatedtrgtGrp ):
						#print "parenting {0} to {1}".format( eachTweak, eachTarget )
						cmds.parent( eachTweak, eachTarget )
				
				# PointConstraints each controller created to each selected object.
				cmds.pointConstraint( control, eachSel, mo=True )
				print control, '>>>', eachSel
				
	#----------------------------------------
	#	Selects all Created Controllers.
	#----------------------------------------
	#TBA
	

	def function( self, *args ):
		''' Controller creation function. '''
		self.variables()

		# For the hierarchy definition.
		self.lastCreatedControl = None
		
		# For the tweakable hierarchy definition.
		self.lastCreatedtwkGrp= []
		self.lastCreatedtrgtGrp= []
		
		# Single controller:
		if self.chexBox == True:

			# Single controller, single iteration:
			if self.snapBox == False:
				for i in range(1):

					self.nameBuffer(  )
					self.createControl( )

			# Snap enabled, Single controller, multiple iterations:
			if self.snapBox == True:

				positions = []

				if self.AboveAlphabet == True:
					self.alpha = self.selection
					
				for self.index, self.eachSel in enumerate( zip( self.selection, self.alpha ) ):
					if self.AboveAlphabet == False:
						self.eachAlpha = self.eachSel[1]
				
					position = cmds.xform( self.eachSel[0], ws=1, m=1, q=1 )


					if self.selectionType == 'clusterHandle':
						position = cmds.xform( self.eachSel[0], ws=1, rp=1, q=1 )

					positions.append(position)
					
					self.nameBuffer(  )
					self.createControl( )
					self.hierarchy(  )

				for eachCtl, eachGrp, eachPosition, eachSel in zip( self.ctlList, self.grpList, positions, self.selection ):
					
					cmds.xform( eachGrp, ws=1, m=eachPosition )
					control= eachCtl

					# If True, this function will be ON.
					self.tweakHiearchy( eachGrp, eachCtl, eachPosition, eachSel )
					
						
					# Constraints or connections queried. 
					if not self.option == self.menuItems[2]:
						self.constraints( control, eachSel )



		# Snap enabled Multiple iterations, multLayer control..
		if self.snapBox == True:
			# Multi layered controller.
			if self.chexBox == False:

				positions=[]

				for self.index, self.eachSel in enumerate( self.selection ):
					position = cmds.xform( self.eachSel, ws=1, m=1, q=1 )
					
					if self.selectionType == 'clusterHandle':
						position = cmds.xform( self.eachSel, ws=1, rp=1, q=1 )
						
					positions.append(position)


					self.nameBuffer(  )
					self.createLayerControl(  )
					self.hierarchy(  )
					self.tweakHiearchy( self.grpList[0], self.ctlList[2], position, self.eachSel )

					cmds.xform( self.grpList[0], ws=1, m=position )

					# Constraints or connections queried. 
					if not self.option == self.menuItems[2]:
						self.constraints( self.ctlList[2], self.eachSel )
							
		if self.snapBox == False:
			if self.chexBox == False:
				self.selection = ['None']
				for self.index, self.eachSel in enumerate( self.selection ):

					self.nameBuffer( )
					self.createLayerControl( )

