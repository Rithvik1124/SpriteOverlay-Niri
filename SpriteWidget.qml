import QtQuick
import Quickshell
import qs.Common
import qs.Widgets
import qs.Modules.Plugins

PluginComponent {
    id: root

    property string pidFile: "/tmp/dms-sprite.pid"

    // Convert file URL to real path
    property string spritePath: {
        var url = Qt.resolvedUrl("sprite.py")
        return url.toString().replace("file://", "")
    }

    function toggle() {
        console.log("Running sprite from:", spritePath)

        Quickshell.execDetached([
            "sh",
            "-c",
            "PIDFILE=" + pidFile + "; \
             if [ -f $PIDFILE ] && kill -0 $(cat $PIDFILE) 2>/dev/null; then \
                 kill $(cat $PIDFILE) && rm -f $PIDFILE; \
             else \
                 GTK_A11Y=none \"" + spritePath + "\" & echo $! > $PIDFILE; \
             fi"
        ])
    }

    horizontalBarPill: Component {
        MouseArea {
            implicitWidth: root.iconSize + 10
            implicitHeight: root.iconSize + 10
            cursorShape: Qt.PointingHandCursor
            onClicked: root.toggle()

            DankIcon {
                anchors.centerIn: parent
                name: "image"
                size: root.iconSize
                color: Theme.primary
            }
        }
    }

    verticalBarPill: Component {
        MouseArea {
            implicitWidth: root.iconSize + 10
            implicitHeight: root.iconSize + 10
            cursorShape: Qt.PointingHandCursor
            onClicked: root.toggle()

            DankIcon {
                anchors.centerIn: parent
                name: "image"
                size: root.iconSize
                color: Theme.primary
            }
        }
    }
}
