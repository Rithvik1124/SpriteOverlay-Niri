import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.platform 1.1

Item {
    id: root
    width: 28
    height: 28

    property bool running: false

    Process {
        id: spriteProcess
        program: "/usr/bin/bash"
        arguments: ["-c", "GTK_A11Y=none ~/.local/bin/sprite.py"]
        running: false

        onRunningChanged: {
            root.running = running
        }
    }

    function toggle() {
        if (spriteProcess.running) {
            spriteProcess.kill()
        } else {
            spriteProcess.start()
        }
    }

    Rectangle {
        anchors.fill: parent
        radius: 6
        color: running ? "#66bb6a" : "#555"
        opacity: 0.2
    }

    Text {
        anchors.centerIn: parent
        text: "🎞"
        font.pixelSize: 16
    }

    MouseArea {
        anchors.fill: parent
        onClicked: toggle()
    }
}
