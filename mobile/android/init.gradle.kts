allprojects {
    buildscript {
        configurations.classpath {
            resolutionStrategy {
                force("com.android.tools.build:gradle:8.11.1")
            }
        }
    }
}
