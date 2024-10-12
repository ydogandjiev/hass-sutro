"""Todo list platform for Sutro."""
from homeassistant.components.todo import TodoListEntity, TodoItem, TodoItemStatus, TodoListEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .const import NAME
from .entity import SutroEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the todo list for the Sutro integration."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([RecommendationsList(coordinator, entry)])


class RecommendationsList(SutroEntity, TodoListEntity):
    """Representation of a Recommendations Todo List."""

    _attr_has_entity_name = True
    _attr_supported_features = TodoListEntityFeature.UPDATE_TODO_ITEM

    def __init__(self, coordinator, entry) -> None:
        """Initialize RecommendationsList."""
        super().__init__(coordinator=coordinator, config_entry=entry)
        self._attr_name = f"{NAME} Recommendations"

    @property
    def unique_id(self):
        """Return a unique ID to use for the list."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-recommendations"

    @property
    def todo_items(self):
        """Return the todo items of the list."""
        if self.coordinator.data is None:
            return None
        else:
            items = []
            for recommendation in self.coordinator.data["me"]["pool"]["latestRecommendations"]["recommendations"]:
                recommendation_status = TodoItemStatus.NEEDS_ACTION if recommendation["completedAt"] is None else TodoItemStatus.COMPLETED
                items.append(TodoItem(
                    summary=recommendation["treatment"],
                    description=recommendation["explanation"],
                    uid=recommendation["id"],
                    status=recommendation_status
                ))

            return items

    async def async_update_todo_item(self, item: TodoItem) -> None:
        """Update an item to the To-do list."""
        if item.status == TodoItemStatus.COMPLETED:
            await self.coordinator.api.async_complete_recommendation(item.uid)
        else:
            await self.coordinator.api.async_uncomplete_recommendation(item.uid)
        await self.coordinator.async_refresh()
