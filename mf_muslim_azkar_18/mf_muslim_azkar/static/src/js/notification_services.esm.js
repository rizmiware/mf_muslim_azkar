/** @odoo-module **/
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { EventBus } from "@odoo/owl";

export const webNotificationService = {
    dependencies: ["action", "bus_service", "notification"],

    start(env, { action, bus_service, notification }) {
        const bus = new EventBus();
        let webNotifTimeouts = {};
        const azkarSound = new Audio('/mf_muslim_azkar/static/src/sound/door-knock.mp3');
        const salahSound = new Audio('/mf_muslim_azkar/static/src/sound/salah.mp3');

        function playNotificationSound() {
            azkarSound.play().catch((error) => {
                console.error("Notification sound failed to play:", error);
            });
        }

        function playAzanSound() {
            salahSound.play().catch((error) => {
                console.error("Azan sound failed to play:", error);
            });
        }

        function displayWebNotification(notifications) {
            Object.values(webNotifTimeouts).forEach((notif) => browser.clearTimeout(notif));
            webNotifTimeouts = {};
            notifications.forEach((notif, index) => {
                webNotifTimeouts[index] = browser.setTimeout(() => {
                    notification.add(notif.message, {
                        title: notif.title,
                        type: notif.type,
                        sticky: notif.sticky,
                        className: notif.className,
                    });
                }, 0);
            });
        }

        bus_service.addEventListener('notification', ({ detail: notifications }) => {
            for (const { payload, type } of notifications) {
                if (type === "muslim.azkar") {
                    playNotificationSound();
                    displayWebNotification(payload);
                } else if (type === "muslim.azan") {
                    playAzanSound();
                    displayWebNotification(payload);
                }
            }
        });

        bus_service.start();

        return {
            addEventListener: bus.addEventListener.bind(bus),
            removeEventListener: bus.removeEventListener.bind(bus),
            trigger: bus.trigger.bind(bus),
        };
    },
};

registry.category("services").add("webNotification", webNotificationService);
