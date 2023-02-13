ymaps.ready(() => {
  const WS_URL = `ws://${window.location.host}/map/`;
  const ticksSocket = new WebSocket(WS_URL);
  var myMap = new ymaps.Map("map", {
    center: [55.753994, 37.622093],
    zoom: 10,
    // Добавим панель маршрутизации.
    controls: ["routePanelControl"],
  });

	// Прослушка сокета
  ticksSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.info(data);
    const { routes } = data;

    if (routes?.length) {

			// Для каджого маршрута создаём новый мультироут
      routes.forEach((route) => {
        const referencePoints = route.current_stops.map(
          (stop) => `${stop.station.lon}, ${stop.station.lat}`
        );

				// До объявления условия надо придумать как чистить все маршруты.
				const multiRoute = new ymaps.multiRouter.MultiRoute({referencePoints});

				// Добавление маршрута
        myMap.geoObjects.add(multiRoute);


				// Активируем последний добавленный маршрут
        multiRoute.events.once("update",() => {
          var routes = multiRoute.getRoutes();
          for (var i = 0, l = routes.getLength(); i < l; i++) {
            var route = routes.get(i);
            if (!route.properties.get("blocked")) {
              multiRoute.setActiveRoute(route);
              route.balloon.open();
              break;
            }
          }
        });
      });
    }
  };
});
