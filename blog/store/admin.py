from django.contrib import admin
from store import models
import zipfile
import os
from apk import APK

# Register your models here.

class AppAdmin(admin.ModelAdmin):
    exclude = ('package', 'version',)
    def save_model(self, request, obj, form, change):
        zipFile=zipfile.ZipFile(obj.apk)
        #read package and version
        manifest=zipFile.read('AndroidManifest.xml')
        parser = APK(manifest)
        obj.package = parser.getPackage()
        obj.version = parser.getVersion()

        #save
        obj.save()
        
        #save icon
        icon=zipFile.read('res/drawable-hdpi/ic_launcher.png')
        outIcon=os.path.join(os.path.dirname(obj.apk.path), obj.package+'.png')
        fp=open(outIcon, 'w')
        fp.write(icon)
        fp.close()


admin.site.register(models.App, AppAdmin)

