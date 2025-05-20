/** @odoo-module **/
import {browser} from "@web/core/browser/browser";
console.log("browser", browser);
import {registry} from "@web/core/registry";

export const webNotificationService = {
    dependencies: ["action", "bus_service", "notification"],

    start(env, {action, bus_service, notification}) {
        let webNotifTimeouts = {};
        const azkarSound = new Audio('mf_muslim_azkar/static/src/sound/door-knock.mp3'); // Add the path to your sound file
        const salahSound = new Audio('mf_muslim_azkar/static/src/sound/salah.mp3'); // Add the path to your sound file

        bus_service.addEventListener('notification', ({ detail: notifications }) => {
            for (const {payload, type} of notifications) {
                console.log("payload", payload);
                console.log("type", type);
                if (type === "muslim.azkar") {
                    playNotificationSound(); // Play sound
                    displaywebNotification(payload);
                }
                if (type === "muslim.azan") {
                    playAzanSound(); // Play sound
                    displaywebNotification(payload);
                }
            }
        });
        bus_service.start();

        function playNotificationSound() {
            azkarSound.play().catch((error) => {
                console.error("Notification sound failed to play:", error);
            });
        }
        function playAzanSound() {
            salahSound.play().catch((error) => {
                console.error("Notification sound failed to play:", error);
            });
        }

        function displaywebNotification(notifications) {
            Object.values(webNotifTimeouts).forEach((notif) =>
                browser.clearTimeout(notif)
            );
            webNotifTimeouts = {};
            notifications.forEach(function (notif) {
                browser.setTimeout(function () {
                    notification.add(notif.message, {
                        title: notif.title,
                        type: notif.type,
                        sticky: notif.sticky,
                        className: notif.className
                    });
                });
            });
        }
    },
};
registry.category("services").add("webNotification", webNotificationService);
