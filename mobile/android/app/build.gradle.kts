import java.util.Properties

plugins {
    id("com.android.application")
    id("kotlin-android")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

// 读取签名配置（key.properties 不入库，见 android/.gitignore）
val keystoreProperties = Properties().apply {
    val propsFile = rootProject.file("key.properties")
    if (propsFile.exists()) {
        propsFile.inputStream().use { load(it) }
    }
}

fun getKeystoreProp(name: String): String? =
    keystoreProperties.getProperty(name)?.takeIf { it.isNotBlank() }

android {
    namespace = "com.media.media_app"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_17.toString()
    }

    defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId = "com.media.media_app"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    signingConfigs {
        create("release") {
            keyAlias = getKeystoreProp("keyAlias")
            keyPassword = getKeystoreProp("keyPassword")
            // storeFile 相对于 android/ 根目录（key.properties 中为 app/upload-keystore.jks）
            storeFile = getKeystoreProp("storeFile")?.let { rootProject.file(it) }
            storePassword = getKeystoreProp("storePassword")
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}

flutter {
    source = "../.."
}
