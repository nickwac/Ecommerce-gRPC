from django.contrib import admin
from .models import Review, ReviewHelpful, ReviewImage


class ReviewImageInline(admin.TabularInline):
    """Inline admin for review images."""
    model = ReviewImage
    extra = 0
    fields = ['image', 'caption', 'uploaded_at']
    readonly_fields = ['uploaded_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Review."""
    
    list_display = [
        'id',
        'product',
        'user',
        'rating',
        'title',
        'is_verified_purchase',
        'helpful_count',
        'not_helpful_count',
        'created_at'
    ]
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
    search_fields = ['title', 'comment', 'user__username', 'product__name']
    readonly_fields = ['created_at', 'updated_at', 'helpful_percentage']
    inlines = [ReviewImageInline]
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'user', 'rating', 'title', 'comment')
        }),
        ('Status', {
            'fields': ('is_verified_purchase', 'helpful_count', 'not_helpful_count', 'helpful_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def helpful_percentage(self, obj):
        return f"{obj.helpful_percentage:.1f}%"
    helpful_percentage.short_description = 'Helpful %'


@admin.register(ReviewHelpful)
class ReviewHelpfulAdmin(admin.ModelAdmin):
    """Admin interface for ReviewHelpful."""
    
    list_display = ['id', 'review', 'user', 'is_helpful', 'created_at']
    list_filter = ['is_helpful', 'created_at']
    search_fields = ['review__title', 'user__username']
    readonly_fields = ['created_at']


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    """Admin interface for ReviewImage."""
    
    list_display = ['id', 'review', 'caption', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['review__title', 'caption']
    readonly_fields = ['uploaded_at']
